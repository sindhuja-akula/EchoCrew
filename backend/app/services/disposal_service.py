from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from database.models.disposal_record import DisposalRecord
from database.models.transfer_weighment import TransferWeighment
from database.models.audit_log import AuditLog
from database.models.enums import AuditAction
from app.schemas.disposal import DisposalRecordCreate, DiversionAnalyticsResponse

def record_disposal(db: Session, disposal_in: DisposalRecordCreate, user_id: int) -> DisposalRecord:
    weighment = db.query(TransferWeighment).filter(TransferWeighment.id == disposal_in.weighment_id).first()
    if not weighment:
        raise HTTPException(status_code=404, detail="Weighment not found")

    total_disposed = disposal_in.recycled_weight_kg + disposal_in.composted_weight_kg + disposal_in.landfill_weight_kg
    
    # Allow some tolerance for scale drift, but generally they should be close
    # To be safe, we calculate diversion based on the total net weight from the weighment
    net_weight = weighment.net_weight_kg
    if net_weight <= 0:
        diversion_rate = 0.0
    else:
        diversion_rate = ((disposal_in.recycled_weight_kg + disposal_in.composted_weight_kg) / net_weight) * 100.0

    disposal = DisposalRecord(
        weighment_id=weighment.id,
        facility_name=disposal_in.facility_name,
        facility_type=disposal_in.facility_type,
        recycled_weight_kg=disposal_in.recycled_weight_kg,
        composted_weight_kg=disposal_in.composted_weight_kg,
        landfill_weight_kg=disposal_in.landfill_weight_kg,
        diversion_rate_pct=diversion_rate,
        processed_at=disposal_in.processed_at
    )
    db.add(disposal)
    
    # Audit Log
    audit_log = AuditLog(
        action=AuditAction.DISPOSAL_RECORDED,
        entity_type="disposal_records",
        entity_id=None,
        actor_id=user_id,
        description=f"Disposal recorded at {disposal_in.facility_name} ({disposal_in.facility_type.value}). Diversion Rate: {diversion_rate:.1f}%"
    )
    db.add(audit_log)
    db.commit()
    db.refresh(disposal)

    audit_log.entity_id = disposal.id
    db.commit()
    db.refresh(disposal)

    return disposal

def get_disposals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DisposalRecord).offset(skip).limit(limit).all()

def get_diversion_analytics(db: Session) -> DiversionAnalyticsResponse:
    # Sum net weight from weighments
    total_net = db.query(func.sum(TransferWeighment.net_weight_kg)).scalar() or 0.0
    
    # Sum recovered and landfill from disposals
    total_recycled = db.query(func.sum(DisposalRecord.recycled_weight_kg)).scalar() or 0.0
    total_composted = db.query(func.sum(DisposalRecord.composted_weight_kg)).scalar() or 0.0
    total_landfill = db.query(func.sum(DisposalRecord.landfill_weight_kg)).scalar() or 0.0

    diversion_rate = 0.0
    if total_net > 0:
        diversion_rate = ((total_recycled + total_composted) / total_net) * 100.0

    return DiversionAnalyticsResponse(
        total_net_weight_kg=total_net,
        total_recycled_kg=total_recycled,
        total_composted_kg=total_composted,
        total_landfill_kg=total_landfill,
        overall_diversion_rate_pct=diversion_rate
    )
