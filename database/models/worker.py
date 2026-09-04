from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database.models.base import Base, TimestampMixin
from database.models.enums import WorkerStatus, WorkerVerificationState

class Worker(Base, TimestampMixin):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, unique=True, index=True)
    worker_code = Column(String(30), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    
    status = Column(
        SQLEnum(WorkerStatus, name="worker_status", native_enum=True, values_callable=lambda obj: [e.value for e in obj]),
        default=WorkerStatus.AVAILABLE,
        nullable=False
    )
    verification_state = Column(
        SQLEnum(WorkerVerificationState, name="worker_verification_state", native_enum=True, values_callable=lambda obj: [e.value for e in obj]),
        default=WorkerVerificationState.UNVERIFIED,
        nullable=False
    )
    
    # Safe reference token for identity verification (NO raw Aadhaar)
    identity_ref = Column(String(100), nullable=True)

    user = relationship("User", backref="worker_profile")
    assignments = relationship("WorkAssignment", back_populates="worker")
    compensations = relationship("Compensation", back_populates="worker")

    def __repr__(self):
        return f"<Worker id={self.id} code='{self.worker_code}' status='{self.status}'>"
