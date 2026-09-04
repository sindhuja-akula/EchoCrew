from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from database.models.base import Base, TimestampMixin
from database.models.enums import AuditAction


class AuditLog(Base, TimestampMixin):
    """
    AuditLog records every significant operational event in the system.
    Immutable audit trail — records are written by trusted backend logic only.
    Clients cannot forge audit history.
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    action = Column(
        SQLEnum(AuditAction, name="audit_action", native_enum=True,
                values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        index=True
    )
    entity_type = Column(String(64), nullable=False, index=True)
    entity_id = Column(Integer, nullable=True, index=True)
    actor_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    description = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)  # supports IPv4 and IPv6

    actor = relationship("User", foreign_keys=[actor_id])

    __table_args__ = (
        Index("idx_audit_logs_action", action),
        Index("idx_audit_logs_entity", entity_type, entity_id),
    )

    def __repr__(self):
        return f"<AuditLog id={self.id} action='{self.action}' entity='{self.entity_type}:{self.entity_id}'>"
