from datetime import datetime, timezone
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from geoalchemy2.elements import WKTElement

from database.models import (
    CleaningEvidence, Verification, Compensation, WorkUnit, GarbageReport,
    VerificationStatus, VerificationMethod, CompensationStatus, ReportStatus, WorkUnitStatus
)
from app.schemas.evidence import EvidenceCreate
from app.schemas.verification import VerificationCreate

class VerificationService:
    def submit_evidence(self, db: Session, evidence_in: EvidenceCreate, submitted_by_id: Optional[int] = None) -> CleaningEvidence:
        """Records worker photo evidence (before/progress/after)."""
        unit = db.query(WorkUnit).filter(WorkUnit.id == evidence_in.work_unit_id).first()
        if not unit:
            raise ValueError(f"WorkUnit with ID {evidence_in.work_unit_id} not found.")

        now = datetime.now(timezone.utc)
        location_elem = None
        if evidence_in.latitude and evidence_in.longitude:
            location_elem = WKTElement(f"POINT({evidence_in.longitude} {evidence_in.latitude})", srid=4326)

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
        db.commit()
        db.refresh(evidence)
        return evidence

    def submit_verification(
        self, db: Session, verification_in: VerificationCreate, verifier_id: Optional[int] = None
    ) -> Tuple[Verification, Optional[Compensation]]:
        """
        Processes evidence audit decision.
        If APPROVED, creates a Compensation eligibility record and updates report status to VERIFIED.
        """
        unit = db.query(WorkUnit).filter(WorkUnit.id == verification_in.work_unit_id).first()
        if not unit:
            raise ValueError(f"WorkUnit with ID {verification_in.work_unit_id} not found.")

        now = datetime.now(timezone.utc)
        verification = Verification(
            evidence_id=verification_in.evidence_id,
            work_unit_id=unit.id,
            verifier_id=verifier_id,
            status=verification_in.status,
            method=verification_in.method,
            notes=verification_in.notes,
            verified_at=now
        )
        db.add(verification)
        db.flush()

        compensation = None

        if verification_in.status == VerificationStatus.APPROVED:
            unit.status = WorkUnitStatus.COMPLETED
            if unit.work_order and unit.work_order.report:
                unit.work_order.report.status = ReportStatus.VERIFIED

            # Find active worker from assignment to create compensation record
            if unit.assignments:
                active_assignment = unit.assignments[-1]
                compensation = Compensation(
                    worker_id=active_assignment.worker_id,
                    assignment_id=active_assignment.id,
                    verification_id=verification.id,
                    amount=250.00,  # Standard operational unit base compensation
                    currency="INR",
                    status=CompensationStatus.ELIGIBLE
                )
                db.add(compensation)

        db.commit()
        db.refresh(verification)
        if compensation:
            db.refresh(compensation)

        return verification, compensation

    def list_compensations(
        self, db: Session, worker_id: Optional[int] = None, skip: int = 0, limit: int = 100
    ) -> Tuple[int, List[Compensation]]:
        query = db.query(Compensation)
        if worker_id:
            query = query.filter(Compensation.worker_id == worker_id)
        total = query.count()
        records = query.order_by(Compensation.id.desc()).offset(skip).limit(limit).all()
        return total, records

verification_service = VerificationService()
