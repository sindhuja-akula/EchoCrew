from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from database.models.base import Base, TimestampMixin
from database.models.enums import VerificationStatus, VerificationMethod

class Verification(Base, TimestampMixin):
    """
    Verification preserves an audit trail for work evidence approval/rejection.
    Never uses a plain boolean `is_verified = true`.
    """
    __tablename__ = "verifications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    evidence_id = Column(Integer, ForeignKey("cleaning_evidence.id", ondelete="CASCADE"), nullable=True, index=True)
    work_unit_id = Column(Integer, ForeignKey("work_units.id", ondelete="CASCADE"), nullable=False, index=True)
    verifier_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    status = Column(
        SQLEnum(VerificationStatus, name="verification_status", native_enum=True, values_callable=lambda obj: [e.value for e in obj]),
        default=VerificationStatus.PENDING,
        nullable=False
    )
    method = Column(
        SQLEnum(VerificationMethod, name="verification_method", native_enum=True, values_callable=lambda obj: [e.value for e in obj]),
        default=VerificationMethod.MANUAL,
        nullable=False
    )
    
    notes = Column(Text, nullable=True)
    verified_at = Column(DateTime(timezone=True), nullable=False)

    evidence = relationship("CleaningEvidence", back_populates="verifications")
    work_unit = relationship("WorkUnit", back_populates="verifications")
    verifier = relationship("User", foreign_keys=[verifier_id])
    compensations = relationship("Compensation", back_populates="verification")

    __table_args__ = (
        Index("idx_verifications_status", status),
    )

    def __repr__(self):
        return f"<Verification id={self.id} status='{self.status}' method='{self.method}'>"
