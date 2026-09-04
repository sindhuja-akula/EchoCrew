from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from database.models.base import Base, TimestampMixin
from database.models.enums import FacilityType

class DisposalRecord(Base, TimestampMixin):
    """
    DisposalRecord tracks final waste segregation, material recovery, and processing facility destination.
    Computes Waste Diversion Rate % = (Recycled + Composted) / Net Weight * 100%.
    """
    __tablename__ = "disposal_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    weighment_id = Column(Integer, ForeignKey("transfer_weighments.id", ondelete="CASCADE"), nullable=False, index=True)
    facility_name = Column(String(100), nullable=False)
    facility_type = Column(
        SQLEnum(FacilityType, name="facility_type", native_enum=True, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False
    )
    recycled_weight_kg = Column(Float, nullable=False, default=0.0)
    composted_weight_kg = Column(Float, nullable=False, default=0.0)
    landfill_weight_kg = Column(Float, nullable=False, default=0.0)
    diversion_rate_pct = Column(Float, nullable=False, default=0.0)
    processed_at = Column(DateTime(timezone=True), nullable=False)

    weighment = relationship("TransferWeighment", backref="disposal_records")

    __table_args__ = (
        Index("idx_disposal_records_weighment_id", weighment_id),
        Index("idx_disposal_records_facility_type", facility_type),
    )

    def __repr__(self):
        return f"<DisposalRecord id={self.id} facility='{self.facility_name}' diversion={self.diversion_rate_pct:.1f}%>"
