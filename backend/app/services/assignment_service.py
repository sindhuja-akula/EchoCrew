from datetime import datetime, timezone
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session

from database.models import (
    WorkAssignment, WorkUnit, Worker,
    AssignmentStatus, WorkUnitStatus, WorkOrderStatus, WorkerStatus, AuditAction
)
from app.schemas.assignment import AssignmentCreate, AssignmentStatusUpdate
from app.services.audit_service import audit_service

# Valid lifecycle transitions for assignments
VALID_TRANSITIONS = {
    AssignmentStatus.ASSIGNED: [AssignmentStatus.ACCEPTED, AssignmentStatus.CANCELLED],
    AssignmentStatus.ACCEPTED: [AssignmentStatus.IN_PROGRESS, AssignmentStatus.CANCELLED],
    AssignmentStatus.IN_PROGRESS: [AssignmentStatus.COMPLETED, AssignmentStatus.CANCELLED],
    AssignmentStatus.COMPLETED: [],
    AssignmentStatus.CANCELLED: [],
    AssignmentStatus.PENDING: [AssignmentStatus.ASSIGNED, AssignmentStatus.CANCELLED],
}


class AssignmentService:
    def assign_worker(
        self, db: Session, assignment_in: AssignmentCreate, assigned_by_id: Optional[int] = None
    ) -> WorkAssignment:
        """
        Creates a WorkAssignment linking a Worker to a WorkUnit & WorkOrder.
        Validates worker exists and is eligible.
        """
        worker = db.query(Worker).filter(Worker.id == assignment_in.worker_id).first()
        if not worker:
            raise ValueError(f"Worker with ID {assignment_in.worker_id} not found.")

        # Block inactive/suspended workers
        if worker.status in (WorkerStatus.SUSPENDED, WorkerStatus.OFF_DUTY):
            raise ValueError(f"Worker {worker.id} is {worker.status.value} and cannot be assigned.")

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

        audit_service.log_event(
            db, AuditAction.WORKER_ASSIGNED, "WorkAssignment", None,
            description=f"Worker {worker.id} assigned to WorkUnit {unit.id}"
        )

        db.commit()
        db.refresh(assignment)
        return assignment

    def update_assignment_status(
        self, db: Session, assignment: WorkAssignment, status_update: AssignmentStatusUpdate
    ) -> WorkAssignment:
        """
        Updates assignment status with lifecycle validation.
        Enforces valid transitions only.
        """
        current = assignment.status
        target = status_update.status

        allowed = VALID_TRANSITIONS.get(current, [])
        if target not in allowed:
            raise ValueError(
                f"Invalid status transition: {current.value} -> {target.value}. "
                f"Allowed: {[s.value for s in allowed]}"
            )

        now = datetime.now(timezone.utc)
        assignment.status = target

        if target == AssignmentStatus.ACCEPTED:
            audit_service.log_event(
                db, AuditAction.ASSIGNMENT_ACCEPTED, "WorkAssignment", assignment.id,
                description=f"Worker {assignment.worker_id} accepted assignment {assignment.id}"
            )

        elif target == AssignmentStatus.IN_PROGRESS:
            assignment.started_at = now
            if assignment.work_unit:
                assignment.work_unit.status = WorkUnitStatus.IN_PROGRESS
            if assignment.work_order:
                assignment.work_order.status = WorkOrderStatus.IN_PROGRESS
            audit_service.log_event(
                db, AuditAction.WORK_STARTED, "WorkAssignment", assignment.id,
                description=f"Worker {assignment.worker_id} started work on assignment {assignment.id}"
            )

        elif target == AssignmentStatus.COMPLETED:
            assignment.completed_at = now
            if assignment.work_unit:
                assignment.work_unit.status = WorkUnitStatus.COMPLETED
            if assignment.worker:
                assignment.worker.status = WorkerStatus.AVAILABLE
            audit_service.log_event(
                db, AuditAction.WORK_COMPLETED, "WorkAssignment", assignment.id,
                description=f"Worker {assignment.worker_id} completed assignment {assignment.id}"
            )

        elif target == AssignmentStatus.CANCELLED:
            if assignment.worker:
                assignment.worker.status = WorkerStatus.AVAILABLE
            audit_service.log_event(
                db, AuditAction.ASSIGNMENT_CANCELLED, "WorkAssignment", assignment.id,
                description=f"Assignment {assignment.id} cancelled"
            )

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


assignment_service = AssignmentService()
