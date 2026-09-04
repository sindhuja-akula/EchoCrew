import uuid
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from geoalchemy2.elements import WKTElement

from database.models import (
    WorkOrder, WorkUnit, GarbageReport,
    WorkOrderStatus, WorkUnitStatus, ReportStatus, AuditAction
)
from app.schemas.work_order import WorkOrderCreate
from app.services.audit_service import audit_service


class WorkOrderService:
    def create_work_order(self, db: Session, work_order_in: WorkOrderCreate) -> WorkOrder:
        """
        Dispatches a cleanup work order for an approved GarbageReport.
        Generates WorkOrder entity and initial WorkUnit.
        """
        report = db.query(GarbageReport).filter(GarbageReport.id == work_order_in.report_id).first()
        if not report:
            raise ValueError(f"GarbageReport with ID {work_order_in.report_id} not found.")

        work_code = f"WO-{uuid.uuid4().hex[:6].upper()}"
        work_order = WorkOrder(
            report_id=report.id,
            work_code=work_code,
            classification=work_order_in.classification,
            required_worker_count=work_order_in.required_worker_count,
            status=WorkOrderStatus.OPEN
        )
        db.add(work_order)
        db.flush()

        # Update report status to ASSIGNED
        report.status = ReportStatus.ASSIGNED

        # Create primary WorkUnit for this order
        unit_code = f"WU-{uuid.uuid4().hex[:6].upper()}-A"
        point_wkt = f"POINT({report.longitude} {report.latitude})"
        work_unit = WorkUnit(
            work_order_id=work_order.id,
            unit_code=unit_code,
            sequence_number=1,
            status=WorkUnitStatus.PENDING,
            latitude=report.latitude,
            longitude=report.longitude,
            location=WKTElement(point_wkt, srid=4326)
        )
        db.add(work_unit)

        audit_service.log_event(
            db, AuditAction.WORK_ORDER_CREATED, "WorkOrder", work_order.id,
            description=f"Work order {work_code} created for report {report.id}"
        )

        db.commit()
        db.refresh(work_order)
        return work_order

    def get_work_order_by_id(self, db: Session, work_order_id: int) -> Optional[WorkOrder]:
        return db.query(WorkOrder).filter(WorkOrder.id == work_order_id).first()

    def list_work_orders(
        self,
        db: Session,
        status: Optional[WorkOrderStatus] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[int, List[WorkOrder]]:
        query = db.query(WorkOrder)
        if status:
            query = query.filter(WorkOrder.status == status)
        total = query.count()
        orders = query.order_by(WorkOrder.id.desc()).offset(skip).limit(limit).all()
        return total, orders


work_order_service = WorkOrderService()
