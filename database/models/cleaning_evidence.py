from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship

try:
    from geoalchemy2 import Geometry
except ImportError:
    from sqlalchemy.types import UserDefinedType
    class Geometry(UserDefinedType):
        def __init__(self, geometry_type="POINT", srid=4326, **kwargs):
            self.geometry_type = geometry_type
            self.srid = srid
        def get_col_spec(self, **kw):
            return "GEOMETRY"

from database.models.base import Base, TimestampMixin
from database.models.enums import EvidenceType

class CleaningEvidence(Base, TimestampMixin):
    """
    CleaningEvidence stores structured proof photos (BEFORE, PROGRESS, AFTER)
    captured during worker assignments, separate from citizen reports.
    """
    __tablename__ = "cleaning_evidence"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    work_unit_id = Column(Integer, ForeignKey("work_units.id", ondelete="CASCADE"), nullable=False, index=True)
    work_assignment_id = Column(Integer, ForeignKey("work_assignments.id", ondelete="SET NULL"), nullable=True, index=True)
    submitted_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    evidence_type = Column(
        SQLEnum(EvidenceType, name="evidence_type", native_enum=True, values_callable=lambda obj: [e.value for e in obj]),
        default=EvidenceType.AFTER,
        nullable=False
    )
    image_url = Column(String(512), nullable=False)
    captured_at = Column(DateTime(timezone=True), nullable=False)
    
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    location = Column(Geometry(geometry_type="POINT", srid=4326), nullable=True)

    work_unit = relationship("WorkUnit", back_populates="evidence_items")
    assignment = relationship("WorkAssignment", back_populates="evidence_items")
    submitted_by = relationship("User", foreign_keys=[submitted_by_id])
    verifications = relationship("Verification", back_populates="evidence")

    __table_args__ = (
        Index("idx_cleaning_evidence_type", evidence_type),
        Index("idx_cleaning_evidence_location", location, postgresql_using="gist"),
    )

    def __repr__(self):
        return f"<CleaningEvidence id={self.id} type='{self.evidence_type}' url='{self.image_url}'>"
