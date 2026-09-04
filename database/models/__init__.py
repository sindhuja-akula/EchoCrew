from database.models.base import Base, TimestampMixin

# Phase 1 — Core
from database.models.enums import (
    UserRole, WasteCategory, VolumeTier, ReportStatus,
    # Phase 2 enums
    WorkerStatus, WorkerVerificationState,
    WorkOrderStatus, WorkUnitStatus, AssignmentStatus,
    EvidenceType, VerificationStatus, VerificationMethod,
    CompensationStatus, CollectionBatchStatus, VehicleStatus,
    # Audit
    AuditAction,
)
from database.models.user import User
from database.models.garbage_report import GarbageReport
from database.models.waste import WASTE_CATEGORY_METADATA, VOLUME_TIER_DESCRIPTORS

# Phase 2 — Operational
from database.models.worker import Worker
from database.models.vehicle import Vehicle
from database.models.work_order import WorkOrder
from database.models.work_unit import WorkUnit
from database.models.work_assignment import WorkAssignment
from database.models.cleaning_evidence import CleaningEvidence
from database.models.verification import Verification
from database.models.compensation import Compensation
from database.models.collection_batch import CollectionBatch
from database.models.audit_log import AuditLog

__all__ = [
    # Base
    "Base",
    "TimestampMixin",
    # Phase 1 Enums
    "UserRole",
    "WasteCategory",
    "VolumeTier",
    "ReportStatus",
    # Phase 2 Enums
    "WorkerStatus",
    "WorkerVerificationState",
    "WorkOrderStatus",
    "WorkUnitStatus",
    "AssignmentStatus",
    "EvidenceType",
    "VerificationStatus",
    "VerificationMethod",
    "CompensationStatus",
    "CollectionBatchStatus",
    "VehicleStatus",
    # Phase 1 Models
    "User",
    "GarbageReport",
    "WASTE_CATEGORY_METADATA",
    "VOLUME_TIER_DESCRIPTORS",
    # Phase 2 Models
    "Worker",
    "Vehicle",
    "WorkOrder",
    "WorkUnit",
    "WorkAssignment",
    "CleaningEvidence",
    "Verification",
    "Compensation",
    "CollectionBatch",
    "AuditLog",
    "AuditAction",
]
