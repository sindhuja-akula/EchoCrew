from fastapi import APIRouter

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

@router.get("/")
def list_vehicles():
    return [{"id": 1, "callsign": "Truck-01", "type": "Utility Truck", "status": "deployed"}]
