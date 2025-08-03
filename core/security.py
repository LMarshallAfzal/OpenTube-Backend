from datetime import datetime, timedelta
from jose import JWTError, jwt
from core.config import settings


def create_access_token(data: dict):
    expires = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {**data, "exp": expires},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
