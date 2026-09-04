import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME", "EchoCrew / CleanLoop Backend")
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "cleanloop_super_secret_development_key_2026")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://cleanloop:cleanloop_password@postgres:5432/cleanloop"
    )

    # Storage settings
    STORAGE_DIR: Path = Path(os.getenv("STORAGE_DIR", "/app/storage"))
    UPLOADS_DIR: Path = Path(os.getenv("UPLOADS_DIR", "/app/storage/uploads"))
    MAX_UPLOAD_SIZE_MB: int = 10
    
    # MinIO / Object Storage Settings
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "minio:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minio_cleanloop_key")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minio_cleanloop_secret")
    MINIO_BUCKET_NAME: str = os.getenv("MINIO_BUCKET_NAME", "cleanloop-evidence")

settings = Settings()
