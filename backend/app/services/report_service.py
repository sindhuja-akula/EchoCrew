from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2.elements import WKTElement
from geoalchemy2.functions import ST_DWithin, ST_Distance, ST_SetSRID, ST_MakePoint

from database.models import GarbageReport, ReportStatus, WasteCategory, VolumeTier
from app.schemas.report import ReportCreate, ReportResponse, SpatialDeduplicationResult
from app.utils.validation import validate_coordinates, haversine_distance_meters

class ReportService:
    def check_spatial_deduplication(
        self,
        db: Session,
        latitude: float,
        longitude: float,
        radius_meters: float = 20.0
    ) -> SpatialDeduplicationResult:
        """
        Checks if a report already exists within 20 meters of the submitted coordinates.
        Supports both PostGIS spatial queries and Python Haversine calculation fallback.
        """
        # Query active reports (not completed/verified)
        active_statuses = [
            ReportStatus.REPORTED,
            ReportStatus.UNDER_REVIEW,
            ReportStatus.APPROVED,
            ReportStatus.ASSIGNED,
            ReportStatus.IN_PROGRESS
        ]

        # 1. Attempt PostGIS spatial query using ST_DWithin / geography
        try:
            target_point = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
            
            # Query reports within geography radius
            existing = db.query(
                GarbageReport,
                ST_Distance(
                    func.ST_GeographyFromText(func.ST_AsText(GarbageReport.location)),
                    func.ST_GeographyFromText(f"SRID=4326;POINT({longitude} {latitude})")
                ).label("distance")
            ).filter(
                GarbageReport.status.in_(active_statuses),
                ST_DWithin(
                    func.ST_GeographyFromText(func.ST_AsText(GarbageReport.location)),
                    func.ST_GeographyFromText(f"SRID=4326;POINT({longitude} {latitude})"),
                    radius_meters
                )
            ).order_by("distance").first()

            if existing:
                report_obj, distance_val = existing
                return SpatialDeduplicationResult(
                    is_duplicate=True,
                    distance_meters=round(float(distance_val), 2),
                    existing_report_id=report_obj.id,
                    existing_report_status=report_obj.status.value if hasattr(report_obj.status, 'value') else str(report_obj.status)
                )
        except Exception:
            # 2. Fallback: Python Haversine distance loop over active reports
            db.rollback()
            active_reports = db.query(GarbageReport).filter(GarbageReport.status.in_(active_statuses)).all()
            for r in active_reports:
                dist = haversine_distance_meters(latitude, longitude, r.latitude, r.longitude)
                if dist <= radius_meters:
                    return SpatialDeduplicationResult(
                        is_duplicate=True,
                        distance_meters=round(dist, 2),
                        existing_report_id=r.id,
                        existing_report_status=r.status.value if hasattr(r.status, 'value') else str(r.status)
                    )

        return SpatialDeduplicationResult(is_duplicate=False)

    def create_report(
        self,
        db: Session,
        report_data: ReportCreate,
        reporter_id: Optional[int] = None
    ) -> Tuple[GarbageReport, SpatialDeduplicationResult]:
        """
        Ingests a new garbage report into PostGIS database.
        Checks for 20m spatial deduplication before saving.
        """
        # Validate spatial coordinates
        is_valid, msg = validate_coordinates(report_data.latitude, report_data.longitude)
        if not is_valid:
            raise ValueError(msg)

        # Check 20-meter spatial deduplication
        dedup_result = self.check_spatial_deduplication(
            db, report_data.latitude, report_data.longitude, radius_meters=20.0
        )

        # Build PostGIS POINT WKT
        point_wkt = f"POINT({report_data.longitude} {report_data.latitude})"

        report = GarbageReport(
            reporter_id=reporter_id,
            description=report_data.description,
            latitude=report_data.latitude,
            longitude=report_data.longitude,
            location=WKTElement(point_wkt, srid=4326),
            category=report_data.category,
            volume_tier=report_data.volume_tier,
            status=ReportStatus.REPORTED,
            image_url=report_data.image_url
        )

        db.add(report)
        db.flush()

        from database.models.enums import AuditAction
        from app.services.audit_service import audit_service
        audit_service.log_event(
            db, AuditAction.REPORT_CREATED, "GarbageReport", report.id,
            actor_id=reporter_id,
            description=f"Garbage report {report.id} created ({report.category.value if hasattr(report.category, 'value') else report.category})"
        )

        db.commit()
        db.refresh(report)

        return report, dedup_result

    def get_report_by_id(self, db: Session, report_id: int) -> Optional[GarbageReport]:
        """Fetch report by primary key ID."""
        return db.query(GarbageReport).filter(GarbageReport.id == report_id).first()

    def list_reports(
        self,
        db: Session,
        status: Optional[ReportStatus] = None,
        category: Optional[WasteCategory] = None,
        volume_tier: Optional[VolumeTier] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[int, List[GarbageReport]]:
        """List garbage reports with optional filters."""
        query = db.query(GarbageReport)

        if status:
            query = query.filter(GarbageReport.status == status)
        if category:
            query = query.filter(GarbageReport.category == category)
        if volume_tier:
            query = query.filter(GarbageReport.volume_tier == volume_tier)

        total = query.count()
        reports = query.order_by(GarbageReport.created_at.desc()).offset(skip).limit(limit).all()
        return total, reports

report_service = ReportService()
