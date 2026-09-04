from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from database.models.enums import AssignmentStatus
from app.schemas.assignment import AssignmentCreate, AssignmentStatusUpdate, AssignmentResponse
from app.services.dispatch_service import dispatch_service

router = APIRouter()

@router.post("/assignments", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
def create_assignment(assignment_in: AssignmentCreate, db: Session = Depends(get_db)):
    """Assigns a worker to a specific WorkUnit."""
    try:
        return dispatch_service.assign_worker(db, assignment_in)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@router.get("/assignments", response_model=List[AssignmentResponse])
def list_assignments(
    worker_id: Optional[int] = Query(None),
    status: Optional[AssignmentStatus] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Lists worker assignments."""
    _, assignments = dispatch_service.list_assignments(db, worker_id=worker_id, status=status, skip=skip, limit=limit)
    return assignments

@router.patch("/assignments/{assignment_id}/status", response_model=AssignmentResponse)
def update_assignment_status(assignment_id: int, status_in: AssignmentStatusUpdate, db: Session = Depends(get_db)):
    """Worker updates assignment status (accepted, in_progress, completed)."""
    assignment = dispatch_service.get_assignment_by_id(db, assignment_id)
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"WorkAssignment with ID {assignment_id} not found.")
    return dispatch_service.update_assignment_status(db, assignment, status_in)
