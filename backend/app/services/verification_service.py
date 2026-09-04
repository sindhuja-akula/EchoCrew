from datetime import datetime, timezone
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session

from database.models import (
    Verification, Compensation, WorkUnit, GarbageReport,
    VerificationStatus, VerificationMethod, ReportStatus, WorkUnitStatus, AuditAction
)
from app.schemas.verification import VerificationCreate
from app.services.compensation_service import compensation_service
from app.services.audit_service import audit_service

class VerificationService:
    def submit_verification(
        self, db: Session, verification_in: VerificationCreate, verifier_id: Optional[int] = None
    ) -> Tuple[Verification, Optional[Compensation]]:
        """
        Processes evidence audit decision.
        If APPROVED, creates a Compensation eligibility record and updates report status to VERIFIED.
        Logs audit events for approval or rejection.
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

            # Find active worker from assignment to create compensation record via compensation_service
            if unit.assignments:
                active_assignment = unit.assignments[-1]
                compensation = compensation_service.create_eligibility(
                    db=db,
                    worker_id=active_assignment.worker_id,
                    assignment_id=active_assignment.id,
                    verification_id=verification.id,
                    amount=250.00,
                    currency="INR"
                )

            audit_service.log_event(
                db, AuditAction.VERIFICATION_APPROVED, "Verification", verification.id,
                actor_id=verifier_id,
                description=f"Verification approved for WorkUnit {unit.id}"
            )

        elif verification_in.status == VerificationStatus.REJECTED:
            audit_service.log_event(
                db, AuditAction.VERIFICATION_REJECTED, "Verification", verification.id,
                actor_id=verifier_id,
                description=f"Verification rejected for WorkUnit {unit.id}: {verification_in.notes or 'No reason provided'}"
            )

        db.commit()
        db.refresh(verification)
        if compensation:
            db.refresh(compensation)

        return verification, compensation

    def get_verification_by_id(self, db: Session, verification_id: int) -> Optional[Verification]:
        return db.query(Verification).filter(Verification.id == verification_id).first()

    def list_verifications(
        self, db: Session, work_unit_id: Optional[int] = None, skip: int = 0, limit: int = 100
    ) -> Tuple[int, List[Verification]]:
        query = db.query(Verification)
        if work_unit_id:
            query = query.filter(Verification.work_unit_id == work_unit_id)
        total = query.count()
        records = query.order_by(Verification.id.desc()).offset(skip).limit(limit).all()
        return total, records

verification_service = VerificationService()
