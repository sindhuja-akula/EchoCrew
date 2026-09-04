from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from database.models.enums import CompensationStatus
from app.schemas.compensation import CompensationResponse, CompensationStatusUpdate
from app.services.compensation_service import compensation_service

router = APIRouter()

@router.get("/compensations", response_model=List[CompensationResponse])
def list_compensations(
    worker_id: Optional[int] = Query(None),
    status: Optional[CompensationStatus] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Lists compensation eligibility records for verified work."""
    _, records = compensation_service.list_compensations(
        db, worker_id=worker_id, status=status, skip=skip, limit=limit
    )
    return records

@router.get("/compensations/{comp_id}", response_model=CompensationResponse)
def get_compensation(comp_id: int, db: Session = Depends(get_db)):
    """Retrieves compensation record by ID."""
    comp = compensation_service.get_compensation_by_id(db, comp_id)
    if not comp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Compensation with ID {comp_id} not found.")
    return comp

@router.patch("/compensations/{comp_id}/status", response_model=CompensationResponse)
def update_compensation_status(comp_id: int, status_in: CompensationStatusUpdate, db: Session = Depends(get_db)):
    """Updates compensation status (eligible -> processing -> paid/rejected). No actual payment."""
    comp = compensation_service.get_compensation_by_id(db, comp_id)
    if not comp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Compensation with ID {comp_id} not found.")
    return compensation_service.update_compensation_status(db, comp, status_in.status)
