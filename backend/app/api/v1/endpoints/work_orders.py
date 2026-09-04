from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from database.models.enums import WorkOrderStatus
from app.schemas.work_order import WorkOrderCreate, WorkOrderResponse
from app.services.dispatch_service import dispatch_service

router = APIRouter()

@router.post("/work-orders", response_model=WorkOrderResponse, status_code=status.HTTP_201_CREATED)
def create_work_order(order_in: WorkOrderCreate, db: Session = Depends(get_db)):
    """Dispatches a cleanup work order for an approved report."""
    try:
        return dispatch_service.create_work_order(db, order_in)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@router.get("/work-orders", response_model=List[WorkOrderResponse])
def list_work_orders(
    status: Optional[WorkOrderStatus] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Lists dispatched work orders."""
    _, orders = dispatch_service.list_work_orders(db, status=status, skip=skip, limit=limit)
    return orders

@router.get("/work-orders/{work_order_id}", response_model=WorkOrderResponse)
def get_work_order(work_order_id: int, db: Session = Depends(get_db)):
    """Retrieves work order details with sub-units."""
    order = dispatch_service.get_work_order_by_id(db, work_order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"WorkOrder with ID {work_order_id} not found.")
    return order
