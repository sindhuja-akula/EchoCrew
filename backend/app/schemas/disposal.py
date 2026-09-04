from pydantic import BaseModel, Field
from datetime import datetime
from database.models.enums import FacilityType

class DisposalRecordCreate(BaseModel):
    weighment_id: int
    facility_name: str
    facility_type: FacilityType
    recycled_weight_kg: float = Field(0.0, ge=0.0)
    composted_weight_kg: float = Field(0.0, ge=0.0)
    landfill_weight_kg: float = Field(0.0, ge=0.0)
    processed_at: datetime

class DisposalRecordResponse(BaseModel):
    id: int
    weighment_id: int
    facility_name: str
    facility_type: FacilityType
    recycled_weight_kg: float
    composted_weight_kg: float
    landfill_weight_kg: float
    diversion_rate_pct: float
    processed_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DiversionAnalyticsResponse(BaseModel):
    total_net_weight_kg: float
    total_recycled_kg: float
    total_composted_kg: float
    total_landfill_kg: float
    overall_diversion_rate_pct: float
