from typing import Optional, List, Tuple
from sqlalchemy.orm import Session

from database.models import Compensation, CompensationStatus, AuditAction
from app.services.audit_service import audit_service


class CompensationService:
    def create_eligibility(
        self,
        db: Session,
        worker_id: int,
        assignment_id: int,
        verification_id: int,
        amount: float = 250.00,
        currency: str = "INR"
    ) -> Compensation:
        """Creates a compensation eligibility record. No actual payment."""
        compensation = Compensation(
            worker_id=worker_id,
            assignment_id=assignment_id,
            verification_id=verification_id,
            amount=amount,
            currency=currency,
            status=CompensationStatus.ELIGIBLE
        )
        db.add(compensation)

        audit_service.log_event(
            db, AuditAction.COMPENSATION_ELIGIBLE, "Compensation", None,
            description=f"Worker {worker_id} eligible for {amount} {currency} compensation"
        )

        db.flush()
        return compensation

    def get_compensation_by_id(self, db: Session, comp_id: int) -> Optional[Compensation]:
        return db.query(Compensation).filter(Compensation.id == comp_id).first()

    def list_compensations(
        self,
        db: Session,
        worker_id: Optional[int] = None,
        status: Optional[CompensationStatus] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[int, List[Compensation]]:
        query = db.query(Compensation)
        if worker_id:
            query = query.filter(Compensation.worker_id == worker_id)
        if status:
            query = query.filter(Compensation.status == status)
        total = query.count()
        records = query.order_by(Compensation.id.desc()).offset(skip).limit(limit).all()
        return total, records

    def update_compensation_status(
        self, db: Session, compensation: Compensation, new_status: CompensationStatus
    ) -> Compensation:
        """Updates compensation status (eligible -> processing -> paid/rejected). No actual payment."""
        compensation.status = new_status
        db.commit()
        db.refresh(compensation)
        return compensation


compensation_service = CompensationService()
