import uuid
from datetime import datetime, timezone
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from geoalchemy2.elements import WKTElement

from database.models import (
    WorkOrder, WorkUnit, WorkAssignment, GarbageReport, Worker,
    WorkOrderStatus, WorkUnitStatus, AssignmentStatus, ReportStatus, WorkerStatus
)
from app.schemas.work_order import WorkOrderCreate
from app.schemas.assignment import AssignmentCreate, AssignmentStatusUpdate

class DispatchService:
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

    def assign_worker(self, db: Session, assignment_in: AssignmentCreate, assigned_by_id: Optional[int] = None) -> WorkAssignment:
        """
        Creates a WorkAssignment linking a Worker to a WorkUnit & WorkOrder.
        """
        worker = db.query(Worker).filter(Worker.id == assignment_in.worker_id).first()
        if not worker:
            raise ValueError(f"Worker with ID {assignment_in.worker_id} not found.")

        unit = db.query(WorkUnit).filter(WorkUnit.id == assignment_in.work_unit_id).first()
        if not unit:
            raise ValueError(f"WorkUnit with ID {assignment_in.work_unit_id} not found.")

        now = datetime.now(timezone.utc)
        assignment = WorkAssignment(
            worker_id=worker.id,
            work_unit_id=unit.id,
            work_order_id=unit.work_order_id,
            assigned_by_id=assigned_by_id,
            status=AssignmentStatus.ASSIGNED,
            assigned_at=now
        )
        db.add(assignment)

        # Update statuses
        worker.status = WorkerStatus.ASSIGNED
        unit.status = WorkUnitStatus.ASSIGNED
        if unit.work_order:
            unit.work_order.status = WorkOrderStatus.ASSIGNED

        db.commit()
        db.refresh(assignment)
        return assignment

    def update_assignment_status(
        self, db: Session, assignment: WorkAssignment, status_update: AssignmentStatusUpdate
    ) -> WorkAssignment:
        """
        Updates assignment status (accepted, in_progress, completed) and triggers lifecycle updates.
        """
        now = datetime.now(timezone.utc)
        assignment.status = status_update.status

        if status_update.status == AssignmentStatus.IN_PROGRESS:
            assignment.started_at = now
            if assignment.work_unit:
                assignment.work_unit.status = WorkUnitStatus.IN_PROGRESS
            if assignment.work_order:
                assignment.work_order.status = WorkOrderStatus.IN_PROGRESS

        elif status_update.status == AssignmentStatus.COMPLETED:
            assignment.completed_at = now
            if assignment.work_unit:
                assignment.work_unit.status = WorkUnitStatus.COMPLETED
            if assignment.worker:
                assignment.worker.status = WorkerStatus.AVAILABLE

        db.commit()
        db.refresh(assignment)
        return assignment

    def get_assignment_by_id(self, db: Session, assignment_id: int) -> Optional[WorkAssignment]:
        return db.query(WorkAssignment).filter(WorkAssignment.id == assignment_id).first()

    def list_assignments(
        self,
        db: Session,
        worker_id: Optional[int] = None,
        status: Optional[AssignmentStatus] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[int, List[WorkAssignment]]:
        query = db.query(WorkAssignment)
        if worker_id:
            query = query.filter(WorkAssignment.worker_id == worker_id)
        if status:
            query = query.filter(WorkAssignment.status == status)

        total = query.count()
        assignments = query.order_by(WorkAssignment.id.desc()).offset(skip).limit(limit).all()
        return total, assignments

dispatch_service = DispatchService()
