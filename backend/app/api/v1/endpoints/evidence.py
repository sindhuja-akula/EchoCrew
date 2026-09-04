from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.evidence import EvidenceCreate, EvidenceResponse
from app.services.evidence_service import evidence_service

router = APIRouter()

@router.post("/evidence", response_model=EvidenceResponse, status_code=status.HTTP_201_CREATED)
def submit_evidence(evidence_in: EvidenceCreate, db: Session = Depends(get_db)):
    """Worker submits photo proof evidence (before/progress/after)."""
    try:
        return evidence_service.submit_evidence(db, evidence_in)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@router.get("/evidence", response_model=List[EvidenceResponse])
def list_evidence(
    work_unit_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Lists evidence records filtered by work unit."""
    _, items = evidence_service.list_evidence(db, work_unit_id=work_unit_id, skip=skip, limit=limit)
    return items

@router.get("/evidence/{evidence_id}", response_model=EvidenceResponse)
def get_evidence(evidence_id: int, db: Session = Depends(get_db)):
    """Retrieves evidence details by ID."""
    evidence = evidence_service.get_evidence_by_id(db, evidence_id)
    if not evidence:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Evidence with ID {evidence_id} not found.")
    return evidence
