from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.transfer_weighment import WeighmentCreate, WeighmentResponse
from app.services import transfer_service

router = APIRouter()

@router.post("/", response_model=WeighmentResponse)
def create_weighment(
    weighment_in: WeighmentCreate,
    db: Session = Depends(get_db)
):
    """
    Record a new weighbridge weighment for a collection batch.
    """
    return transfer_service.record_weighment(db=db, weighment_in=weighment_in, user_id=1)

@router.get("/", response_model=List[WeighmentResponse])
def read_weighments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve weighments.
    """
    return transfer_service.get_weighments(db=db, skip=skip, limit=limit)

@router.get("/{weighment_id}", response_model=WeighmentResponse)
def read_weighment(
    weighment_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific weighment by ID.
    """
    return transfer_service.get_weighment(db=db, weighment_id=weighment_id)
