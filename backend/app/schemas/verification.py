from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from database.models.enums import VerificationStatus, VerificationMethod

class VerificationCreate(BaseModel):
    work_unit_id: int = Field(..., description="Work Unit ID to verify")
    evidence_id: Optional[int] = Field(None, description="Cleaning Evidence ID being evaluated")
    status: VerificationStatus = Field(VerificationStatus.APPROVED, description="Verification status decision")
    method: VerificationMethod = Field(VerificationMethod.MANUAL, description="Verification method")
    notes: Optional[str] = Field(None, description="Supervisor or verifier audit notes")

class VerificationResponse(BaseModel):
    id: int
    evidence_id: Optional[int] = None
    work_unit_id: int
    verifier_id: Optional[int] = None
    status: VerificationStatus
    method: VerificationMethod
    notes: Optional[str] = None
    verified_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
