from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from fastapi import HTTPException

from database.models.garbage_report import GarbageReport
from database.models.work_assignment import WorkAssignment
from database.models.cleaning_evidence import CleaningEvidence
from database.models.audit_log import AuditLog
from database.models.enums import AuditAction, VerificationStatus
from app.schemas.intelligent_verification import IntelligentVerificationRequest, IntelligentVerificationResponse

def evaluate_correspondence(db: Session, request: IntelligentVerificationRequest, user_id: int) -> IntelligentVerificationResponse:
    # Fetch entities
    report = db.query(GarbageReport).filter(GarbageReport.id == request.report_id).first()
    assignment = db.query(WorkAssignment).filter(WorkAssignment.id == request.assignment_id).first()
    evidence = db.query(CleaningEvidence).filter(CleaningEvidence.id == request.evidence_id).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")

    # 1. Location Correspondence
    # Compute spatial distance in meters using PostGIS ST_DistanceSphere
    distance_meters = 0.0
    if report.location is not None and evidence.location is not None:
        distance = db.query(func.ST_DistanceSphere(report.location, evidence.location)).scalar()
        distance_meters = distance if distance is not None else 0.0

    # Tolerance: 50 meters
    location_match = distance_meters <= 50.0

    # 2. Time Correspondence
    # Check if evidence capture time is within assignment start/end (or nearby)
    # Using assignment.created_at and updated_at as proxy if accepted_at/started_at are not easily available,
    # but let's check assignment fields. WorkAssignment has accepted_at, completed_at?
    # We can just check the time difference between assignment update and evidence capture.
    time_delta_minutes = 0.0
    if assignment.updated_at and evidence.captured_at:
        delta = abs((evidence.captured_at - assignment.updated_at).total_seconds())
        time_delta_minutes = delta / 60.0

    # Tolerance: Evidence captured within 120 minutes of assignment activity
    time_match = time_delta_minutes <= 120.0

    # 3. Overall Score Calculation
    score = 0.0
    if location_match:
        score += 60.0
    else:
        # partial score for location
        score += max(0, 60.0 - (distance_meters - 50.0) * 0.5)

    if time_match:
        score += 40.0
    else:
        # partial score for time
        score += max(0, 40.0 - (time_delta_minutes - 120.0) * 0.5)
        
    score = min(100.0, max(0.0, score))

    # 4. Recommended Status
    if score >= 85.0:
        recommended_status = VerificationStatus.APPROVED
    elif score < 40.0:
        recommended_status = VerificationStatus.REJECTED
    else:
        recommended_status = VerificationStatus.REQUIRES_REVIEW

    # Log Audit Event
    audit_log = AuditLog(
        action=AuditAction.INTELLIGENT_VERIFICATION_EVALUATED,
        entity_type="cleaning_evidence",
        entity_id=evidence.id,
        actor_id=user_id,
        description=f"AI Verification: Score {score:.1f}% (Dist: {distance_meters:.1f}m, Time: {time_delta_minutes:.1f}m). Recommendation: {recommended_status.value}"
    )
    db.add(audit_log)
    db.commit()

    return IntelligentVerificationResponse(
        location_match=location_match,
        distance_meters=distance_meters,
        time_match=time_match,
        time_delta_minutes=time_delta_minutes,
        correspondence_score=score,
        recommended_status=recommended_status
    )
