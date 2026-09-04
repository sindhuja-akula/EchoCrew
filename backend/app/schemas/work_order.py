from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from database.models.enums import WorkOrderStatus
from app.schemas.work_unit import WorkUnitResponse

class WorkOrderCreate(BaseModel):
    report_id: int = Field(..., description="Approved Garbage Report ID to dispatch")
    classification: str = Field("GENERAL_CLEANUP", description="Cleanup job classification")
    required_worker_count: int = Field(1, ge=1, description="Number of workers required")

class WorkOrderStatusUpdate(BaseModel):
    status: WorkOrderStatus

class WorkOrderResponse(BaseModel):
    id: int
    report_id: int
    work_code: str
    classification: str
    required_worker_count: int
    status: WorkOrderStatus
    created_at: datetime
    updated_at: datetime
    units: List[WorkUnitResponse] = []

    class Config:
        from_attributes = True
