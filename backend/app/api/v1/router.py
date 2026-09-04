from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    reports,
    workers,
    vehicles,
    work_orders,
    assignments,
    evidence,
    verification,
    compensation,
    collections,
    audit
)

api_v1_router = APIRouter()

api_v1_router.include_router(health.router, tags=["Health"])
api_v1_router.include_router(reports.router, tags=["Reports"])
api_v1_router.include_router(workers.router, tags=["Workers"])
api_v1_router.include_router(vehicles.router, tags=["Vehicles"])
api_v1_router.include_router(work_orders.router, tags=["Work Orders"])
api_v1_router.include_router(assignments.router, tags=["Assignments"])
api_v1_router.include_router(evidence.router, tags=["Evidence"])
api_v1_router.include_router(verification.router, tags=["Verification"])
api_v1_router.include_router(compensation.router, tags=["Compensation"])
api_v1_router.include_router(collections.router, tags=["Collections"])
api_v1_router.include_router(audit.router, tags=["Audit"])
