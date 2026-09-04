from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from database.models.enums import WasteCategory, VolumeTier, ReportStatus
from app.utils.validation import validate_coordinates

class ReportBase(BaseModel):
    description: Optional[str] = Field(None, description="Detailed text description of the waste accumulation site")
    latitude: float = Field(..., description="Latitude coordinate in WGS 84 (-90 to 90)")
    longitude: float = Field(..., description="Longitude coordinate in WGS 84 (-180 to 180)")
    category: WasteCategory = Field(WasteCategory.MIXED, description="Category of waste (wet, dry, electronic, clothing, hazardous, mixed, other)")
    volume_tier: VolumeTier = Field(VolumeTier.MODERATE, description="Estimated volume tier (minor, moderate, bulk)")

    @field_validator("latitude", "longitude")
    @classmethod
    def check_coordinates(cls, v: float, info) -> float:
        field_name = info.field_name
        if field_name == "latitude" and not (-90.0 <= v <= 90.0):
            raise ValueError(f"Latitude must be between -90 and 90 degrees. Got {v}")
        if field_name == "longitude" and not (-180.0 <= v <= 180.0):
            raise ValueError(f"Longitude must be between -180 and 180 degrees. Got {v}")
        return v

class ReportCreate(ReportBase):
    image_url: Optional[str] = Field(None, description="URL or file path to uploaded site photo")

class ReportResponse(ReportBase):
    id: int
    reporter_id: Optional[int] = None
    status: ReportStatus
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    # Operational metadata
    is_spatial_duplicate: bool = False
    duplicate_of_report_id: Optional[int] = None

    class Config:
        from_attributes = True

class SpatialDeduplicationCheck(BaseModel):
    latitude: float
    longitude: float
    radius_meters: float = 20.0

class SpatialDeduplicationResult(BaseModel):
    is_duplicate: bool
    distance_meters: Optional[float] = None
    existing_report_id: Optional[int] = None
    existing_report_status: Optional[str] = None

class ReportListResponse(BaseModel):
    total: int
    reports: List[ReportResponse]
