from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from database.models.enums import CompensationStatus

class CompensationResponse(BaseModel):
    id: int
    worker_id: int
    assignment_id: int
    verification_id: Optional[int] = None
    amount: float
    currency: str = "INR"
    status: CompensationStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
