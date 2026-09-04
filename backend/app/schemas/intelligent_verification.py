from pydantic import BaseModel, Field
from database.models.enums import VerificationStatus

class IntelligentVerificationRequest(BaseModel):
    report_id: int
    assignment_id: int
    evidence_id: int

class IntelligentVerificationResponse(BaseModel):
    location_match: bool
    distance_meters: float = Field(..., description="Distance between report and evidence in meters")
    time_match: bool
    time_delta_minutes: float = Field(..., description="Time difference between assignment window and evidence capture")
    correspondence_score: float = Field(..., description="Confidence score from 0 to 100%")
    recommended_status: VerificationStatus
