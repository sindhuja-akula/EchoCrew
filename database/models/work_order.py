from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from database.models.base import Base, TimestampMixin
from database.models.enums import WorkOrderStatus

class WorkOrder(Base, TimestampMixin):
    __tablename__ = "work_orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    report_id = Column(Integer, ForeignKey("garbage_reports.id", ondelete="RESTRICT"), nullable=False, index=True)
    work_code = Column(String(30), unique=True, nullable=False, index=True)
    classification = Column(String(50), nullable=False, default="GENERAL_CLEANUP")
    required_worker_count = Column(Integer, nullable=False, default=1)
    
    status = Column(
        SQLEnum(WorkOrderStatus, name="work_order_status", native_enum=True, values_callable=lambda obj: [e.value for e in obj]),
        default=WorkOrderStatus.OPEN,
        nullable=False
    )

    report = relationship("GarbageReport", backref="work_orders")
    units = relationship("WorkUnit", back_populates="work_order", cascade="all, delete-orphan")
    assignments = relationship("WorkAssignment", back_populates="work_order")

    __table_args__ = (
        Index("idx_work_orders_status", status),
    )

    def __repr__(self):
        return f"<WorkOrder id={self.id} code='{self.work_code}' status='{self.status}'>"
