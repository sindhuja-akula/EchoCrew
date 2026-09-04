from fastapi import APIRouter

router = APIRouter(prefix="/hotspots", tags=["hotspots"])

@router.get("/")
def list_hotspots():
    return [{"id": 1, "location": "Zone A", "risk_level": "high"}]
