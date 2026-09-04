from fastapi import APIRouter
from app.api.v1 import (
    auth,
    reports,
    hotspots,
    tasks,
    crews,
    vehicles,
    dashboard,
    users
)

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(reports.router)
api_router.include_router(hotspots.router)
api_router.include_router(tasks.router)
api_router.include_router(crews.router)
api_router.include_router(vehicles.router)
api_router.include_router(dashboard.router)
api_router.include_router(users.router)
