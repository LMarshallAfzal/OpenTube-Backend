from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from services.auth import authenticate_user, create_user
from db.session import get_db
from core.security import create_access_token
from pydantic import BaseModel

router = APIRouter()


# Add these Pydantic models
class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


@router.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, user_data.username, user_data.password)
    return {"token": create_access_token({"sub": user.username})}


@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": create_access_token({"sub": user.username})}
