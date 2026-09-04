from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WeighmentCreate(BaseModel):
    batch_id: int
    weighbridge_code: str
    gross_weight_kg: float
    tare_weight_kg: float
    weighment_time: datetime

class WeighmentResponse(BaseModel):
    id: int
    batch_id: int
    weighbridge_code: str
    gross_weight_kg: float
    tare_weight_kg: float
    net_weight_kg: float
    weighment_time: datetime
    operator_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
