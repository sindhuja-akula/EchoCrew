from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from database.models.enums import CollectionBatchStatus

class CollectionBatchCreate(BaseModel):
    vehicle_id: Optional[int] = Field(None, description="Transport Vehicle ID")
    total_volume_m3: float = Field(..., ge=0.0, description="Total aggregated waste volume in m³")

class CollectionBatchStatusUpdate(BaseModel):
    status: CollectionBatchStatus

class CollectionBatchResponse(BaseModel):
    id: int
    batch_code: str
    vehicle_id: Optional[int] = None
    status: CollectionBatchStatus
    total_volume_m3: float
    collected_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
