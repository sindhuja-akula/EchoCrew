import uuid
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from database.models import Vehicle, VehicleStatus
from app.schemas.vehicle import VehicleCreate, VehicleStatusUpdate

class VehicleService:
    def create_vehicle(self, db: Session, vehicle_in: VehicleCreate) -> Vehicle:
        """Register fleet vehicle."""
        code = vehicle_in.vehicle_code or f"TRK-{uuid.uuid4().hex[:4].upper()}"
        vehicle = Vehicle(
            vehicle_code=code,
            callsign=vehicle_in.callsign,
            license_plate=vehicle_in.license_plate,
            vehicle_type=vehicle_in.vehicle_type,
            capacity_m3=vehicle_in.capacity_m3,
            status=VehicleStatus.AVAILABLE
        )
        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)
        return vehicle

    def get_vehicle_by_id(self, db: Session, vehicle_id: int) -> Optional[Vehicle]:
        return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    def list_vehicles(
        self,
        db: Session,
        status: Optional[VehicleStatus] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[int, List[Vehicle]]:
        query = db.query(Vehicle)
        if status:
            query = query.filter(Vehicle.status == status)
        total = query.count()
        vehicles = query.order_by(Vehicle.id.desc()).offset(skip).limit(limit).all()
        return total, vehicles

    def update_vehicle_status(self, db: Session, vehicle: Vehicle, status_update: VehicleStatusUpdate) -> Vehicle:
        vehicle.status = status_update.status
        db.commit()
        db.refresh(vehicle)
        return vehicle

vehicle_service = VehicleService()
