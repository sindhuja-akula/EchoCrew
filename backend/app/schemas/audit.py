from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from database.models.enums import AuditAction

class AuditLogResponse(BaseModel):
    id: int
    action: AuditAction
    entity_type: str
    entity_id: Optional[int] = None
    actor_id: Optional[int] = None
    description: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
