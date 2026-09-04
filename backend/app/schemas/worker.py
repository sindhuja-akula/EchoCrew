from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from database.models.enums import WorkerStatus, WorkerVerificationState

class WorkerBase(BaseModel):
    phone: Optional[str] = Field(None, description="Worker contact phone number")
    identity_ref: Optional[str] = Field(None, description="Safe identity token (e.g. hash/ref ID)")

class WorkerCreate(WorkerBase):
    user_id: Optional[int] = Field(None, description="User account ID associated with worker")
    worker_code: Optional[str] = Field(None, description="Custom worker code (auto-generated if omitted)")

class WorkerStatusUpdate(BaseModel):
    status: WorkerStatus
    verification_state: Optional[WorkerVerificationState] = None

class WorkerResponse(WorkerBase):
    id: int
    user_id: Optional[int] = None
    worker_code: str
    status: WorkerStatus
    verification_state: WorkerVerificationState
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
