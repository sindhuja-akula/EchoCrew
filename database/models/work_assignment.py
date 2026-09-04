from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from database.models.base import Base, TimestampMixin
from database.models.enums import AssignmentStatus

class WorkAssignment(Base, TimestampMixin):
    """
    WorkAssignment maps Workers to WorkUnits / WorkOrders.
    Supports assigning multiple workers to a large job.
    """
    __tablename__ = "work_assignments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    worker_id = Column(Integer, ForeignKey("workers.id", ondelete="CASCADE"), nullable=False, index=True)
    work_unit_id = Column(Integer, ForeignKey("work_units.id", ondelete="CASCADE"), nullable=False, index=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id", ondelete="CASCADE"), nullable=False, index=True)
    assigned_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    status = Column(
        SQLEnum(AssignmentStatus, name="assignment_status", native_enum=True, values_callable=lambda obj: [e.value for e in obj]),
        default=AssignmentStatus.ASSIGNED,
        nullable=False
    )
    
    assigned_at = Column(DateTime(timezone=True), nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    worker = relationship("Worker", back_populates="assignments")
    work_unit = relationship("WorkUnit", back_populates="assignments")
    work_order = relationship("WorkOrder", back_populates="assignments")
    assigned_by = relationship("User", foreign_keys=[assigned_by_id])
    evidence_items = relationship("CleaningEvidence", back_populates="assignment")
    compensations = relationship("Compensation", back_populates="assignment")

    __table_args__ = (
        Index("idx_work_assignments_status", status),
    )

    def __repr__(self):
        return f"<WorkAssignment id={self.id} worker_id={self.worker_id} status='{self.status}'>"
