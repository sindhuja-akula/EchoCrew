from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from database.models.enums import WorkerStatus, WorkerVerificationState
from app.schemas.worker import WorkerCreate, WorkerStatusUpdate, WorkerResponse
from app.services.worker_service import worker_service

router = APIRouter()

@router.post("/workers", response_model=WorkerResponse, status_code=status.HTTP_201_CREATED)
def create_worker(worker_in: WorkerCreate, db: Session = Depends(get_db)):
    """Registers a new cleanup crew worker profile."""
    return worker_service.create_worker(db, worker_in)

@router.get("/workers", response_model=List[WorkerResponse])
def list_workers(
    status: Optional[WorkerStatus] = Query(None),
    verification_state: Optional[WorkerVerificationState] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Lists workers with optional status filters."""
    _, workers = worker_service.list_workers(
        db, status=status, verification_state=verification_state, skip=skip, limit=limit
    )
    return workers

@router.get("/workers/{worker_id}", response_model=WorkerResponse)
def get_worker(worker_id: int, db: Session = Depends(get_db)):
    """Retrieves worker details by ID."""
    worker = worker_service.get_worker_by_id(db, worker_id)
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Worker with ID {worker_id} not found.")
    return worker

@router.patch("/workers/{worker_id}/status", response_model=WorkerResponse)
def update_worker_status(worker_id: int, status_in: WorkerStatusUpdate, db: Session = Depends(get_db)):
    """Updates worker availability status or verification state."""
    worker = worker_service.get_worker_by_id(db, worker_id)
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Worker with ID {worker_id} not found.")
    return worker_service.update_worker_status(db, worker, status_in)
