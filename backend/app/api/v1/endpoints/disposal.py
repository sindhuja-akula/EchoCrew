from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.disposal import DisposalRecordCreate, DisposalRecordResponse, DiversionAnalyticsResponse
from app.services import disposal_service

router = APIRouter()

@router.post("/", response_model=DisposalRecordResponse)
def create_disposal_record(
    disposal_in: DisposalRecordCreate,
    db: Session = Depends(get_db)
):
    """
    Record waste segregation and processing destination.
    """
    return disposal_service.record_disposal(db=db, disposal_in=disposal_in, user_id=1)

@router.get("/", response_model=List[DisposalRecordResponse])
def read_disposal_records(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve disposal records.
    """
    return disposal_service.get_disposals(db=db, skip=skip, limit=limit)

@router.get("/analytics/summary", response_model=DiversionAnalyticsResponse)
def get_diversion_analytics(
    db: Session = Depends(get_db)
):
    """
    Get waste diversion analytics and recycling rates.
    """
    return disposal_service.get_diversion_analytics(db=db)
