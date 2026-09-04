from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/metrics")
def get_dashboard_metrics():
    return {
        "active_crews": 4,
        "pending_tasks": 12,
        "hotspots_detected": 3,
        "system_status": "operational"
    }
