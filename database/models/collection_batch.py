from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from database.models.base import Base, TimestampMixin
from database.models.enums import CollectionBatchStatus

class CollectionBatch(Base, TimestampMixin):
    """
    CollectionBatch represents durable batch-level waste transport aggregation
    (Work -> Waste -> Collection Batch -> Transfer Station -> Recycler).
    No fragile paper QR labels on individual bags.
    """
    __tablename__ = "collection_batches"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    batch_code = Column(String(30), unique=True, nullable=False, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="SET NULL"), nullable=True, index=True)

    status = Column(
        SQLEnum(CollectionBatchStatus, name="collection_batch_status", native_enum=True, values_callable=lambda obj: [e.value for e in obj]),
        default=CollectionBatchStatus.COLLECTING,
        nullable=False
    )
    
    total_volume_m3 = Column(Float, nullable=False, default=0.0)
    collected_at = Column(DateTime(timezone=True), nullable=False)

    vehicle = relationship("Vehicle", back_populates="batches")

    __table_args__ = (
        Index("idx_collection_batches_status", status),
    )

    def __repr__(self):
        return f"<CollectionBatch id={self.id} code='{self.batch_code}' volume={self.total_volume_m3}m³ status='{self.status}'>"
