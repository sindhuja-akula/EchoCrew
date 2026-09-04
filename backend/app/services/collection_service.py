import uuid
from datetime import datetime, timezone
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from database.models import CollectionBatch, CollectionBatchStatus
from app.schemas.collection import CollectionBatchCreate, CollectionBatchStatusUpdate

class CollectionService:
    def create_batch(self, db: Session, batch_in: CollectionBatchCreate) -> CollectionBatch:
        """Create waste transport collection batch."""
        code = f"BATCH-{uuid.uuid4().hex[:6].upper()}"
        now = datetime.now(timezone.utc)
        batch = CollectionBatch(
            batch_code=code,
            vehicle_id=batch_in.vehicle_id,
            status=CollectionBatchStatus.COLLECTING,
            total_volume_m3=batch_in.total_volume_m3,
            collected_at=now
        )
        db.add(batch)
        db.commit()
        db.refresh(batch)
        return batch

    def get_batch_by_id(self, db: Session, batch_id: int) -> Optional[CollectionBatch]:
        return db.query(CollectionBatch).filter(CollectionBatch.id == batch_id).first()

    def list_batches(
        self,
        db: Session,
        status: Optional[CollectionBatchStatus] = None,
        vehicle_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[int, List[CollectionBatch]]:
        query = db.query(CollectionBatch)
        if status:
            query = query.filter(CollectionBatch.status == status)
        if vehicle_id:
            query = query.filter(CollectionBatch.vehicle_id == vehicle_id)
        
        total = query.count()
        batches = query.order_by(CollectionBatch.id.desc()).offset(skip).limit(limit).all()
        return total, batches

    def update_batch_status(self, db: Session, batch: CollectionBatch, status_update: CollectionBatchStatusUpdate) -> CollectionBatch:
        batch.status = status_update.status
        db.commit()
        db.refresh(batch)
        return batch

collection_service = CollectionService()
