""" Create and verify JWT tokens """
from datetime import datetime, timedelta
import jwt

from app.core.settings.base import settings


def create_access_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {**data, "exp": expire},
        settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM
    )


def decode_token(token: str) -> dict:
    """Validate and decode JWT"""
    return jwt.decode(
        token,
        settings.SECRET_KEY.get_secret_value(),
        algorithms=[settings.ALGORITHM]
    )
