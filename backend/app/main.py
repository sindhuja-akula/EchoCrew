import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.api.v1.router import api_v1_router

app = FastAPI(
    title=settings.APP_NAME,
    description="EchoCrew / CleanLoop Urban Waste Ingestion & Spatial Operations Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure local storage directories exist and mount static file directory
storage_path = settings.STORAGE_DIR
storage_path.mkdir(parents=True, exist_ok=True)
uploads_path = settings.UPLOADS_DIR
uploads_path.mkdir(parents=True, exist_ok=True)

app.mount("/storage", StaticFiles(directory=str(storage_path)), name="storage")

# Include API v1 router (/api/v1)
app.include_router(api_v1_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["System"])
def read_root():
    return {
        "status": "online",
        "service": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "api_v1": f"{settings.API_V1_STR}"
    }
