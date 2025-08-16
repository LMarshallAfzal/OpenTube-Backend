from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.services.auth import authenticate_user, create_user
from app.db.session import get_session
from app.core.auth.jwt import create_access_token
from app.schemas.user import UserCreate
from app.schemas.token import TokenResponse

auth_router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@auth_router.post("/register", response_model=TokenResponse)
def signup(
    user_data: UserCreate,
    db: Session = Depends(get_session),
) -> TokenResponse:
    """
    Create a new user and return an access model
    """
    user = create_user(db, user_data.username, user_data.password)

    token = create_access_token({"sub": user.username})
    return TokenResponse(access_token=token, token_type="bearer")


@auth_router.post("/token", response_model=TokenResponse)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session),
) -> TokenResponse:
    """
    Authenticate an existing user and issue a JWT access token
    """
    user = authenticate_user(db, form.username, form.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenResponse(
        access_token=create_access_token({"sub": user.username}),
        token_type="bearer"
    )
