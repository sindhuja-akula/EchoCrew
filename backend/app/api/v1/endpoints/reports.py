from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.core.database import get_db
from database.models.enums import WasteCategory, VolumeTier, ReportStatus
from app.schemas.report import ReportCreate, ReportResponse, ReportListResponse, SpatialDeduplicationResult
from app.services.report_service import report_service
from app.services.storage_service import storage_service

router = APIRouter()

@router.post("/reports", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(
    report_in: ReportCreate,
    db: Session = Depends(get_db)
):
    """
    Submits a new citizen or responder garbage report.
    Checks for 20-meter spatial deduplication before saving to PostGIS database.
    """
    try:
        report, dedup_result = report_service.create_report(db, report_in)
        
        # Build response with spatial deduplication metadata
        response_data = ReportResponse.model_validate(report)
        response_data.is_spatial_duplicate = dedup_result.is_duplicate
        response_data.duplicate_of_report_id = dedup_result.existing_report_id
        return response_data
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to ingest report: {str(e)}"
        )

@router.post("/reports/upload-photo", status_code=status.HTTP_201_CREATED)
async def upload_report_photo(
    file: UploadFile = File(...)
):
    """
    Uploads a site photo for garbage report and returns accessible relative storage URL.
    """
    file_url = await storage_service.save_upload_file(file)
    return {
        "status": "success",
        "image_url": file_url
    }

@router.get("/reports", response_model=ReportListResponse)
def list_reports(
    status: Optional[ReportStatus] = Query(None, description="Filter by report status"),
    category: Optional[WasteCategory] = Query(None, description="Filter by waste category"),
    volume_tier: Optional[VolumeTier] = Query(None, description="Filter by volume tier"),
    skip: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(100, ge=1, le=500, description="Pagination page size"),
    db: Session = Depends(get_db)
):
    """
    Queries citizen garbage reports with optional filtering by status, waste category, or volume tier.
    """
    total, reports = report_service.list_reports(
        db, status=status, category=category, volume_tier=volume_tier, skip=skip, limit=limit
    )

    items = [ReportResponse.model_validate(r) for r in reports]
    return ReportListResponse(total=total, reports=items)

@router.get("/reports/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieves details of a specific garbage report by ID.
    """
    report = report_service.get_report_by_id(db, report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report with ID {report_id} not found."
        )
    return ReportResponse.model_validate(report)
