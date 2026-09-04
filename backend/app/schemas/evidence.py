from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from database.models.enums import EvidenceType

class EvidenceCreate(BaseModel):
    work_unit_id: int = Field(..., description="Work Unit ID for evidence submission")
    work_assignment_id: Optional[int] = Field(None, description="Associated Work Assignment ID")
    evidence_type: EvidenceType = Field(EvidenceType.AFTER, description="Evidence phase (before, progress, after)")
    image_url: str = Field(..., description="Uploaded evidence photo URL")
    latitude: Optional[float] = Field(None, description="GPS capture latitude")
    longitude: Optional[float] = Field(None, description="GPS capture longitude")

class EvidenceResponse(BaseModel):
    id: int
    work_unit_id: int
    work_assignment_id: Optional[int] = None
    submitted_by_id: Optional[int] = None
    evidence_type: EvidenceType
    image_url: str
    captured_at: datetime
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
