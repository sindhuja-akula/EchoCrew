from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.verification import VerificationCreate, VerificationResponse
from app.services.verification_service import verification_service

from app.schemas.intelligent_verification import IntelligentVerificationRequest, IntelligentVerificationResponse
from app.services import intelligent_verification_service

router = APIRouter()

@router.post("/verifications/analyze", response_model=IntelligentVerificationResponse)
def analyze_verification(
    request: IntelligentVerificationRequest,
    db: Session = Depends(get_db)
):
    """
    AI/Automated evaluation of location and time correspondence.
    """
    # Assuming system/default actor if no auth provided in this route for now
    return intelligent_verification_service.evaluate_correspondence(db=db, request=request, user_id=1)

@router.post("/verifications", response_model=VerificationResponse, status_code=status.HTTP_201_CREATED)
def submit_verification(verification_in: VerificationCreate, db: Session = Depends(get_db)):
    """Supervisor/Dispatcher submits evidence verification decision."""
    try:
        verification, _ = verification_service.submit_verification(db, verification_in)
        return verification
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@router.get("/verifications", response_model=List[VerificationResponse])
def list_verifications(
    work_unit_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Lists verification records."""
    _, items = verification_service.list_verifications(db, work_unit_id=work_unit_id, skip=skip, limit=limit)
    return items

@router.get("/verifications/{verification_id}", response_model=VerificationResponse)
def get_verification(verification_id: int, db: Session = Depends(get_db)):
    """Retrieves verification details by ID."""
    verification = verification_service.get_verification_by_id(db, verification_id)
    if not verification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Verification with ID {verification_id} not found.")
    return verification
