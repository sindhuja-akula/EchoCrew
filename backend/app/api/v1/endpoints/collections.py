from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from database.models.enums import CollectionBatchStatus
from app.schemas.collection import CollectionBatchCreate, CollectionBatchStatusUpdate, CollectionBatchResponse
from app.services.collection_service import collection_service

router = APIRouter()

@router.post("/collections", response_model=CollectionBatchResponse, status_code=status.HTTP_201_CREATED)
def create_collection_batch(batch_in: CollectionBatchCreate, db: Session = Depends(get_db)):
    """Creates a durable waste collection transport batch."""
    return collection_service.create_batch(db, batch_in)

@router.get("/collections", response_model=List[CollectionBatchResponse])
def list_collection_batches(
    status: Optional[CollectionBatchStatus] = Query(None),
    vehicle_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Lists waste collection transport batches."""
    _, batches = collection_service.list_batches(db, status=status, vehicle_id=vehicle_id, skip=skip, limit=limit)
    return batches

@router.get("/collections/{batch_id}", response_model=CollectionBatchResponse)
def get_collection_batch(batch_id: int, db: Session = Depends(get_db)):
    """Retrieves waste collection batch details."""
    batch = collection_service.get_batch_by_id(db, batch_id)
    if not batch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"CollectionBatch with ID {batch_id} not found.")
    return batch

@router.patch("/collections/{batch_id}/status", response_model=CollectionBatchResponse)
def update_collection_batch_status(batch_id: int, status_in: CollectionBatchStatusUpdate, db: Session = Depends(get_db)):
    """Updates waste collection transport batch status."""
    batch = collection_service.get_batch_by_id(db, batch_id)
    if not batch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"CollectionBatch with ID {batch_id} not found.")
    return collection_service.update_batch_status(db, batch, status_in)
