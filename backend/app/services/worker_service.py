import uuid
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from database.models import Worker, WorkerStatus, WorkerVerificationState
from app.schemas.worker import WorkerCreate, WorkerStatusUpdate

class WorkerService:
    def create_worker(self, db: Session, worker_in: WorkerCreate) -> Worker:
        """Register new worker profile."""
        code = worker_in.worker_code or f"WRK-{uuid.uuid4().hex[:6].upper()}"
        worker = Worker(
            user_id=worker_in.user_id,
            worker_code=code,
            phone=worker_in.phone,
            identity_ref=worker_in.identity_ref,
            status=WorkerStatus.AVAILABLE,
            verification_state=WorkerVerificationState.UNVERIFIED
        )
        db.add(worker)
        db.commit()
        db.refresh(worker)
        return worker

    def get_worker_by_id(self, db: Session, worker_id: int) -> Optional[Worker]:
        return db.query(Worker).filter(Worker.id == worker_id).first()

    def get_worker_by_code(self, db: Session, code: str) -> Optional[Worker]:
        return db.query(Worker).filter(Worker.worker_code == code).first()

    def list_workers(
        self,
        db: Session,
        status: Optional[WorkerStatus] = None,
        verification_state: Optional[WorkerVerificationState] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[int, List[Worker]]:
        query = db.query(Worker)
        if status:
            query = query.filter(Worker.status == status)
        if verification_state:
            query = query.filter(Worker.verification_state == verification_state)
        
        total = query.count()
        workers = query.order_by(Worker.id.desc()).offset(skip).limit(limit).all()
        return total, workers

    def update_worker_status(self, db: Session, worker: Worker, status_update: WorkerStatusUpdate) -> Worker:
        worker.status = status_update.status
        if status_update.verification_state:
            worker.verification_state = status_update.verification_state
        db.commit()
        db.refresh(worker)
        return worker

worker_service = WorkerService()
