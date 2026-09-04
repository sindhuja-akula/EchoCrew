from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from database.models.enums import AuditAction
from app.schemas.audit import AuditLogResponse
from app.services.audit_service import audit_service

router = APIRouter()

@router.get("/audit", response_model=List[AuditLogResponse])
def list_audit_logs(
    action: Optional[AuditAction] = Query(None),
    entity_type: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Lists audit log records (admin access). Never exposes secrets."""
    _, logs = audit_service.list_audit_logs(
        db, action=action, entity_type=entity_type, skip=skip, limit=limit
    )
    return logs

@router.get("/audit/{audit_id}", response_model=AuditLogResponse)
def get_audit_log(audit_id: int, db: Session = Depends(get_db)):
    """Retrieves a single audit log entry."""
    log = audit_service.get_audit_log_by_id(db, audit_id)
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"AuditLog with ID {audit_id} not found.")
    return log
