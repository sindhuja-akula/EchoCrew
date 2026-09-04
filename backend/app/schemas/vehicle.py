from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from database.models.enums import VehicleStatus

class VehicleBase(BaseModel):
    callsign: str = Field(..., description="Vehicle operational callsign")
    license_plate: str = Field(..., description="Vehicle registration license plate")
    vehicle_type: str = Field("UTILITY_TRUCK", description="Type of vehicle")
    capacity_m3: float = Field(5.0, ge=0.1, description="Volumetric capacity in m³")

class VehicleCreate(VehicleBase):
    vehicle_code: Optional[str] = Field(None, description="Custom vehicle code (auto-generated if omitted)")

class VehicleStatusUpdate(BaseModel):
    status: VehicleStatus

class VehicleResponse(VehicleBase):
    id: int
    vehicle_code: str
    status: VehicleStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
