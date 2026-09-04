import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME", "EchoCrew Backend")
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change_this_super_secret_key_for_dev_only")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://echocrew:echocrew_pass@localhost:5432/echocrew_db")

settings = Settings()
