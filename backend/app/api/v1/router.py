from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    reports,
    workers,
    vehicles,
    work_orders,
    assignments,
    verifications,
    collections
)

api_v1_router = APIRouter()

api_v1_router.include_router(health.router, tags=["Health"])
api_v1_router.include_router(reports.router, tags=["Reports"])
api_v1_router.include_router(workers.router, tags=["Workers"])
api_v1_router.include_router(vehicles.router, tags=["Vehicles"])
api_v1_router.include_router(work_orders.router, tags=["Work Orders"])
api_v1_router.include_router(assignments.router, tags=["Assignments"])
api_v1_router.include_router(verifications.router, tags=["Verifications"])
api_v1_router.include_router(collections.router, tags=["Collections"])
