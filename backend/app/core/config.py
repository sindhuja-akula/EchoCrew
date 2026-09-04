import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME", "EchoCrew")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://echocrew:echocrew_pass@localhost:5432/echocrew_db")

settings = Settings()
