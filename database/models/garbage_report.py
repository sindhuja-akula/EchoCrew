from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship

try:
    from geoalchemy2 import Geometry
except ImportError:
    # Dummy fallback type for environment without geoalchemy2 installed
    from sqlalchemy.types import UserDefinedType
    class Geometry(UserDefinedType):
        def __init__(self, geometry_type="POINT", srid=4326, **kwargs):
            self.geometry_type = geometry_type
            self.srid = srid
        def get_col_spec(self, **kw):
            return "GEOMETRY"

from database.models.base import Base, TimestampMixin
from database.models.enums import WasteCategory, VolumeTier, ReportStatus

class GarbageReport(Base, TimestampMixin):
    __tablename__ = "garbage_reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    reporter_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    description = Column(Text, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # PostGIS Spatial POINT Field (SRID 4326 - WGS 84 Coordinate Reference System)
    location = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)

    category = Column(
        SQLEnum(WasteCategory, name="waste_category", native_enum=True, values_callable=lambda obj: [e.value for e in obj]),
        default=WasteCategory.MIXED,
        nullable=False
    )
    volume_tier = Column(
        SQLEnum(VolumeTier, name="volume_tier", native_enum=True, values_callable=lambda obj: [e.value for e in obj]),
        default=VolumeTier.MODERATE,
        nullable=False
    )
    status = Column(
        SQLEnum(ReportStatus, name="report_status", native_enum=True, values_callable=lambda obj: [e.value for e in obj]),
        default=ReportStatus.REPORTED,
        nullable=False
    )

    image_url = Column(String(512), nullable=True)

    reporter = relationship("User", back_populates="reports")

    __table_args__ = (
        Index("idx_garbage_reports_location", location, postgresql_using="gist"),
        Index("idx_garbage_reports_status", status),
        Index("idx_garbage_reports_created_at", "created_at"),
    )

    def __repr__(self):
        return f"<GarbageReport id={self.id} lat={self.latitude} lon={self.longitude} status='{self.status}'>"
