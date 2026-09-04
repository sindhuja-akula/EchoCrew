from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.config import settings

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint returning system status and PostgreSQL PostGIS database connectivity.
    """
    db_status = "unreachable"
    postgis_version = None

    try:
        result = db.execute(text("SELECT postgis_full_version();")).scalar()
        if result:
            db_status = "connected"
            postgis_version = str(result)[:50]
    except Exception:
        try:
            # Fallback simple connectivity test
            result = db.execute(text("SELECT 1")).scalar()
            if result == 1:
                db_status = "connected"
        except Exception as e:
            db_status = f"error: {str(e)}"

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "service": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "database": {
            "status": db_status,
            "postgis": postgis_version
        }
    }
