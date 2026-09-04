from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from database.models.enums import WorkOrderStatus, WorkUnitStatus

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
