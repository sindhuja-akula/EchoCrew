from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from database.models import AuditLog, AuditAction


class AuditService:
    def log_event(
        self,
        db: Session,
        action: AuditAction,
        entity_type: str,
        entity_id: Optional[int] = None,
        actor_id: Optional[int] = None,
        description: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> AuditLog:
        """Creates an immutable audit log record. Called by trusted backend logic only."""
        audit = AuditLog(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            actor_id=actor_id,
            description=description,
            ip_address=ip_address
        )
        db.add(audit)
        db.flush()
        return audit

    def list_audit_logs(
        self,
        db: Session,
        action: Optional[AuditAction] = None,
        entity_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[int, List[AuditLog]]:
        query = db.query(AuditLog)
        if action:
            query = query.filter(AuditLog.action == action)
        if entity_type:
            query = query.filter(AuditLog.entity_type == entity_type)
        total = query.count()
        logs = query.order_by(AuditLog.id.desc()).offset(skip).limit(limit).all()
        return total, logs

    def get_audit_log_by_id(self, db: Session, audit_id: int) -> Optional[AuditLog]:
        return db.query(AuditLog).filter(AuditLog.id == audit_id).first()


audit_service = AuditService()
