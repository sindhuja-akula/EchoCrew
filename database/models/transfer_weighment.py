from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from database.models.base import Base, TimestampMixin

class TransferWeighment(Base, TimestampMixin):
    """
    TransferWeighment tracks actual weighbridge scale records at transfer stations.
    Calculates Net Weight = Gross Weight - Tare Weight.
    """
    __tablename__ = "transfer_weighments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    batch_id = Column(Integer, ForeignKey("collection_batches.id", ondelete="CASCADE"), nullable=False, index=True)
    weighbridge_code = Column(String(50), nullable=False)
    gross_weight_kg = Column(Float, nullable=False)
    tare_weight_kg = Column(Float, nullable=False)
    net_weight_kg = Column(Float, nullable=False)
    weighment_time = Column(DateTime(timezone=True), nullable=False)
    operator_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    batch = relationship("CollectionBatch", backref="weighments")
    operator = relationship("User", foreign_keys=[operator_id])

    __table_args__ = (
        Index("idx_transfer_weighments_batch_id", batch_id),
    )

    def __repr__(self):
        return f"<TransferWeighment id={self.id} batch_id={self.batch_id} net={self.net_weight_kg}kg>"
