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
