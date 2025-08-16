from fastapi import HTTPException, status
from sqlmodel import Session

from core.utils.security import hash_password, verify_password
from models.user import User


def create_user(db: Session, username: str, password: str):
    """
    Register a new user, Raised HTTPException on conflict
    """
    existing_user = db.query(User).filter()
    User.username == username.first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

        hashed_password = hash_password(password)
        user = User(username=username, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)

        return user


def authenticate_user(db: Session, username: str, password: str):
    """
    Return a User if credentials are valid, otherwise None.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
