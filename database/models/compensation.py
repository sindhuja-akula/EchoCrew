from sqlalchemy import Column, Integer, Float, String, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from database.models.base import Base, TimestampMixin
from database.models.enums import CompensationStatus

class Compensation(Base, TimestampMixin):
    """
    Compensation represents eligibility foundation for completed work.
    NO payment gateway, bank account, or actual money transfer logic in Phase 2.
    """
    __tablename__ = "compensations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    worker_id = Column(Integer, ForeignKey("workers.id", ondelete="CASCADE"), nullable=False, index=True)
    assignment_id = Column(Integer, ForeignKey("work_assignments.id", ondelete="CASCADE"), nullable=False, index=True)
    verification_id = Column(Integer, ForeignKey("verifications.id", ondelete="SET NULL"), nullable=True, index=True)

    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False, default="INR")
    
    status = Column(
        SQLEnum(CompensationStatus, name="compensation_status", native_enum=True, values_callable=lambda obj: [e.value for e in obj]),
        default=CompensationStatus.PENDING,
        nullable=False
    )

    worker = relationship("Worker", back_populates="compensations")
    assignment = relationship("WorkAssignment", back_populates="compensations")
    verification = relationship("Verification", back_populates="compensations")

    __table_args__ = (
        Index("idx_compensations_status", status),
    )

    def __repr__(self):
        return f"<Compensation id={self.id} worker_id={self.worker_id} amount={self.amount} status='{self.status}'>"
