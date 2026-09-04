from fastapi import APIRouter

router = APIRouter(prefix="/crews", tags=["crews"])

@router.get("/")
def list_crews():
    return [{"id": 1, "name": "Alpha Response Crew", "members_count": 5}]
