from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.evidence import EvidenceCreate, EvidenceResponse
from app.schemas.verification import VerificationCreate, VerificationResponse
from app.schemas.compensation import CompensationResponse
from app.services.verification_service import verification_service

router = APIRouter()

@router.post("/evidence", response_model=EvidenceResponse, status_code=status.HTTP_201_CREATED)
def submit_evidence(evidence_in: EvidenceCreate, db: Session = Depends(get_db)):
    """Worker submits photo proof evidence (before/progress/after)."""
    try:
        return verification_service.submit_evidence(db, evidence_in)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@router.post("/verifications", response_model=VerificationResponse, status_code=status.HTTP_201_CREATED)
def submit_verification(verification_in: VerificationCreate, db: Session = Depends(get_db)):
    """Supervisor/Dispatcher submits evidence verification decision."""
    try:
        verification, _ = verification_service.submit_verification(db, verification_in)
        return verification
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@router.get("/compensations", response_model=List[CompensationResponse])
def list_compensations(
    worker_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Lists compensation eligibility records for verified work."""
    _, records = verification_service.list_compensations(db, worker_id=worker_id, skip=skip, limit=limit)
    return records
