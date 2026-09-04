from datetime import datetime, timezone
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from geoalchemy2.elements import WKTElement

from database.models import CleaningEvidence, WorkUnit, AuditAction
from app.schemas.evidence import EvidenceCreate
from app.services.audit_service import audit_service


class EvidenceService:
    def submit_evidence(
        self, db: Session, evidence_in: EvidenceCreate, submitted_by_id: Optional[int] = None
    ) -> CleaningEvidence:
        """Records worker photo evidence (before/progress/after)."""
        unit = db.query(WorkUnit).filter(WorkUnit.id == evidence_in.work_unit_id).first()
        if not unit:
            raise ValueError(f"WorkUnit with ID {evidence_in.work_unit_id} not found.")

        now = datetime.now(timezone.utc)
        location_elem = None
        if evidence_in.latitude and evidence_in.longitude:
            location_elem = WKTElement(
                f"POINT({evidence_in.longitude} {evidence_in.latitude})", srid=4326
            )

        evidence = CleaningEvidence(
            work_unit_id=unit.id,
            work_assignment_id=evidence_in.work_assignment_id,
            submitted_by_id=submitted_by_id,
            evidence_type=evidence_in.evidence_type,
            image_url=evidence_in.image_url,
            captured_at=now,
            latitude=evidence_in.latitude,
            longitude=evidence_in.longitude,
            location=location_elem
        )
        db.add(evidence)

        audit_service.log_event(
            db, AuditAction.EVIDENCE_SUBMITTED, "CleaningEvidence", None,
            description=f"Evidence ({evidence_in.evidence_type.value}) submitted for WorkUnit {unit.id}"
        )

        db.commit()
        db.refresh(evidence)
        return evidence

    def get_evidence_by_id(self, db: Session, evidence_id: int) -> Optional[CleaningEvidence]:
        return db.query(CleaningEvidence).filter(CleaningEvidence.id == evidence_id).first()

    def list_evidence(
        self,
        db: Session,
        work_unit_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[int, List[CleaningEvidence]]:
        query = db.query(CleaningEvidence)
        if work_unit_id:
            query = query.filter(CleaningEvidence.work_unit_id == work_unit_id)
        total = query.count()
        items = query.order_by(CleaningEvidence.id.desc()).offset(skip).limit(limit).all()
        return total, items


evidence_service = EvidenceService()
