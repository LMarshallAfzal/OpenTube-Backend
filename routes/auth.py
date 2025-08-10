from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from services.auth import authenticate_user, create_user
from db.session import get_session
from core.security import create_access_token
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


# Add these Pydantic models
class UserCreate(BaseModel):
    username: str
    password: str


@router.post("/signup")
def signup(
    user_data: UserCreate,
    db: Session = Depends(get_session)
):
    user = create_user(db, user_data.username, user_data.password)
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session),
):
    user = authenticate_user(db, form.username, form.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "access_token": create_access_token({"sub": user.username}),
        "token_type": "bearer"
    }
