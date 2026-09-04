import enum

class UserRole(str, enum.Enum):
    COMMANDER = "commander"
    DISPATCHER = "dispatcher"
    CREW_LEAD = "crew_lead"
    RESPONDER = "responder"
    CITIZEN = "citizen"

class WasteCategory(str, enum.Enum):
    WET = "wet"
    DRY = "dry"
    ELECTRONIC = "electronic"
    CLOTHING = "clothing"
    HAZARDOUS = "hazardous"
    MIXED = "mixed"
    OTHER = "other"

class VolumeTier(str, enum.Enum):
    MINOR = "minor"       # Small bag / household waste (~ < 0.2 m³)
    MODERATE = "moderate"    # Multiple bags / medium pile (~ 0.2 - 1.0 m³)
    BULK = "bulk"        # Large dumping site / truckload (~ > 1.0 m³)

class ReportStatus(str, enum.Enum):
    REPORTED = "reported"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    CLEANED = "cleaned"
    VERIFIED = "verified"

# --- Phase 2 Extensions Enums ---

class WorkerStatus(str, enum.Enum):
    AVAILABLE = "available"
    ASSIGNED = "assigned"
    OFF_DUTY = "off_duty"
    SUSPENDED = "suspended"

class WorkerVerificationState(str, enum.Enum):
    UNVERIFIED = "unverified"
    PENDING_VERIFICATION = "pending_verification"
    VERIFIED = "verified"
    REJECTED = "rejected"

class WorkOrderStatus(str, enum.Enum):
    OPEN = "open"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class WorkUnitStatus(str, enum.Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class AssignmentStatus(str, enum.Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class EvidenceType(str, enum.Enum):
    BEFORE = "before"
    PROGRESS = "progress"
    AFTER = "after"

class VerificationStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REQUIRES_REVIEW = "requires_review"

class VerificationMethod(str, enum.Enum):
    MANUAL = "manual"
    AI_ASSISTED = "ai_assisted"
    SUPERVISOR = "supervisor"

class CompensationStatus(str, enum.Enum):
    PENDING = "pending"
    ELIGIBLE = "eligible"
    PROCESSING = "processing"
    PAID = "paid"
    REJECTED = "rejected"

class CollectionBatchStatus(str, enum.Enum):
    COLLECTING = "collecting"
    SEALED = "sealed"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"

class VehicleStatus(str, enum.Enum):
    AVAILABLE = "available"
    DEPLOYED = "deployed"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"

# --- Phase 3 Extensions Enums ---

class FacilityType(str, enum.Enum):
    RECYCLING_PLANT = "recycling_plant"
    COMPOSTING_FACILITY = "composting_facility"
    WASTE_TO_ENERGY = "waste_to_energy"
    SANITARY_LANDFILL = "sanitary_landfill"

class AuditAction(str, enum.Enum):
    REPORT_CREATED = "report_created"
    WORKER_CREATED = "worker_created"
    WORK_ORDER_CREATED = "work_order_created"
    WORKER_ASSIGNED = "worker_assigned"
    ASSIGNMENT_ACCEPTED = "assignment_accepted"
    WORK_STARTED = "work_started"
    EVIDENCE_SUBMITTED = "evidence_submitted"
    WORK_COMPLETED = "work_completed"
    VERIFICATION_APPROVED = "verification_approved"
    VERIFICATION_REJECTED = "verification_rejected"
    COMPENSATION_ELIGIBLE = "compensation_eligible"
    COLLECTION_BATCH_CREATED = "collection_batch_created"
    VEHICLE_CREATED = "vehicle_created"
    ASSIGNMENT_CANCELLED = "assignment_cancelled"
    INTELLIGENT_VERIFICATION_EVALUATED = "intelligent_verification_evaluated"
    WEIGHMENT_RECORDED = "weighment_recorded"
    WASTE_SEGREGATED = "waste_segregated"
    DISPOSAL_RECORDED = "disposal_recorded"
