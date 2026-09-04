from datetime import datetime, timedelta, timezone
from typing import Optional, Union, Any

def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Generate JWT access token stub."""
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=60))
    return f"mock_jwt_token_for_{subject}_exp_{int(expire.timestamp())}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify standard plain text password against hash stub."""
    return plain_password == hashed_password

def get_password_hash(password: str) -> str:
    """Generate hashed password stub."""
    return f"hashed_{password}"
