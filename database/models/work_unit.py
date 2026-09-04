from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum as SQLEnum, Index
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
from database.models.enums import WorkUnitStatus

class WorkUnit(Base, TimestampMixin):
    """
    WorkUnit represents sub-tasks or partitioned work units for large cleanup jobs
    allowing 1 GarbageReport -> 1 WorkOrder -> N WorkUnits -> N Workers.
    """
    __tablename__ = "work_units"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id", ondelete="CASCADE"), nullable=False, index=True)
    unit_code = Column(String(30), unique=True, nullable=False, index=True)
    sequence_number = Column(Integer, nullable=False, default=1)
    
    status = Column(
        SQLEnum(WorkUnitStatus, name="work_unit_status", native_enum=True, values_callable=lambda obj: [e.value for e in obj]),
        default=WorkUnitStatus.PENDING,
        nullable=False
    )
    
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    location = Column(Geometry(geometry_type="POINT", srid=4326), nullable=True)

    work_order = relationship("WorkOrder", back_populates="units")
    assignments = relationship("WorkAssignment", back_populates="work_unit")
    evidence_items = relationship("CleaningEvidence", back_populates="work_unit")
    verifications = relationship("Verification", back_populates="work_unit")

    __table_args__ = (
        Index("idx_work_units_status", status),
        Index("idx_work_units_location", location, postgresql_using="gist"),
    )

    def __repr__(self):
        return f"<WorkUnit id={self.id} code='{self.unit_code}' status='{self.status}'>"
