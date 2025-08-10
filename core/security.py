from typing import Annotated
from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from core.config import settings
from db.session import get_session
from models.user import User
from schemas.token import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


def create_access_token(data: dict):
    expires = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {**data, "exp": expires},
        settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM
    )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_session),
) -> User:
    """
    Decode JWT, validate it and return corresponding user
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY.get_secret_value(),
                             algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except (jwt.PyJWTError):
        raise credentials_exception
    user = db.query(User.filter(User.username == token_data.username).first())
    if not user:
        raise credentials_exception

    return user
