from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from database.models.enums import VehicleStatus
from app.schemas.vehicle import VehicleCreate, VehicleStatusUpdate, VehicleResponse
from app.services.vehicle_service import vehicle_service

router = APIRouter()

@router.post("/vehicles", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(vehicle_in: VehicleCreate, db: Session = Depends(get_db)):
    """Registers transport fleet equipment vehicle."""
    return vehicle_service.create_vehicle(db, vehicle_in)

@router.get("/vehicles", response_model=List[VehicleResponse])
def list_vehicles(
    status: Optional[VehicleStatus] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Lists fleet vehicles."""
    _, vehicles = vehicle_service.list_vehicles(db, status=status, skip=skip, limit=limit)
    return vehicles

@router.get("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """Retrieves vehicle detail by ID."""
    vehicle = vehicle_service.get_vehicle_by_id(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle with ID {vehicle_id} not found.")
    return vehicle
