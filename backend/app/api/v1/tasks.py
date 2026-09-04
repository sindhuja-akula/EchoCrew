from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/")
def list_tasks():
    return [{"id": 101, "task": "Debris Clearance", "status": "in_progress"}]
