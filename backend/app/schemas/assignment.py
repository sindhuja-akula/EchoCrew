from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from database.models.enums import AssignmentStatus

class AssignmentCreate(BaseModel):
    worker_id: int = Field(..., description="Worker ID to assign")
    work_unit_id: int = Field(..., description="Work Unit ID to assign to worker")

class AssignmentStatusUpdate(BaseModel):
    status: AssignmentStatus

class AssignmentResponse(BaseModel):
    id: int
    worker_id: int
    work_unit_id: int
    work_order_id: int
    assigned_by_id: Optional[int] = None
    status: AssignmentStatus
    assigned_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
