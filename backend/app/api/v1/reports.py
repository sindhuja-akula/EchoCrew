from fastapi import APIRouter

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/")
def list_reports():
    return [{"id": 1, "title": "Field Incident Report", "status": "active"}]

@router.post("/")
def create_report():
    return {"id": 2, "message": "Report submitted"}
