from sqlalchemy import Column, Integer, String, Float, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from database.models.base import Base, TimestampMixin
from database.models.enums import VehicleStatus

class Vehicle(Base, TimestampMixin):
    """
    Vehicle represents transport fleet equipment with volumetric capacity (m³).
    """
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    vehicle_code = Column(String(30), unique=True, nullable=False, index=True)
    callsign = Column(String(50), nullable=False)
    license_plate = Column(String(30), unique=True, nullable=False)
    vehicle_type = Column(String(50), nullable=False, default="UTILITY_TRUCK")
    capacity_m3 = Column(Float, nullable=False, default=5.0)  # Volume in cubic meters

    status = Column(
        SQLEnum(VehicleStatus, name="vehicle_status", native_enum=True, values_callable=lambda obj: [e.value for e in obj]),
        default=VehicleStatus.AVAILABLE,
        nullable=False
    )

    batches = relationship("CollectionBatch", back_populates="vehicle")

    __table_args__ = (
        Index("idx_vehicles_status", status),
    )

    def __repr__(self):
        return f"<Vehicle id={self.id} code='{self.vehicle_code}' capacity={self.capacity_m3}m³ status='{self.status}'>"
