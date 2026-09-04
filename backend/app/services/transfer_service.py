from sqlalchemy.orm import Session
from fastapi import HTTPException
from database.models.transfer_weighment import TransferWeighment
from database.models.collection_batch import CollectionBatch
from database.models.audit_log import AuditLog
from database.models.enums import AuditAction, CollectionBatchStatus
from app.schemas.transfer_weighment import WeighmentCreate

def record_weighment(db: Session, weighment_in: WeighmentCreate, user_id: int) -> TransferWeighment:
    batch = db.query(CollectionBatch).filter(CollectionBatch.id == weighment_in.batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Collection batch not found")

    net_weight = weighment_in.gross_weight_kg - weighment_in.tare_weight_kg
    if net_weight < 0:
        raise HTTPException(status_code=400, detail="Net weight cannot be negative")

    weighment = TransferWeighment(
        batch_id=batch.id,
        weighbridge_code=weighment_in.weighbridge_code,
        gross_weight_kg=weighment_in.gross_weight_kg,
        tare_weight_kg=weighment_in.tare_weight_kg,
        net_weight_kg=net_weight,
        weighment_time=weighment_in.weighment_time,
        operator_id=user_id
    )
    db.add(weighment)

    # Update Batch Status
    batch.status = CollectionBatchStatus.DELIVERED

    # Audit Log
    audit_log = AuditLog(
        action=AuditAction.WEIGHMENT_RECORDED,
        entity_type="transfer_weighments",
        entity_id=None, # Will update after flush
        actor_id=user_id,
        description=f"Weighment recorded for Batch {batch.batch_code}: Gross {weighment_in.gross_weight_kg}kg, Tare {weighment_in.tare_weight_kg}kg, Net {net_weight}kg"
    )
    db.add(audit_log)
    db.commit()
    db.refresh(weighment)

    audit_log.entity_id = weighment.id
    db.commit()
    db.refresh(weighment)

    return weighment

def get_weighments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TransferWeighment).offset(skip).limit(limit).all()

def get_weighment(db: Session, weighment_id: int):
    weighment = db.query(TransferWeighment).filter(TransferWeighment.id == weighment_id).first()
    if not weighment:
        raise HTTPException(status_code=404, detail="Weighment not found")
    return weighment
