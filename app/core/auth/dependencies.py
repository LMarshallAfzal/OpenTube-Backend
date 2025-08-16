""" Dependency that loads current user """
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
import jwt

from app.models.user import User
from app.core.auth.jwt import decode_token
from app.db.session import get_session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


def _get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = _get_user_by_username(db, username)
    if not user:
        raise credentials_exception
    return user
