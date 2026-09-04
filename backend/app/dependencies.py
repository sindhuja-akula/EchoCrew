from typing import Generator
from fastapi import Depends, HTTPException, status
from app.database import get_db

def get_db_dependency() -> Generator:
    return get_db()

def get_current_user_stub():
    """Stub dependency for authenticating user requests."""
    return {"user_id": 1, "username": "admin", "role": "commander"}
