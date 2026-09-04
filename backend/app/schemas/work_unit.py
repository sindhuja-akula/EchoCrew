from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from database.models.enums import WorkUnitStatus

class WorkUnitStatusUpdate(BaseModel):
    status: WorkUnitStatus

class WorkUnitResponse(BaseModel):
    id: int
    work_order_id: int
    unit_code: str
    sequence_number: int
    status: WorkUnitStatus
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
