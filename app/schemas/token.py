from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TokenPayload(BaseModel):
    """
    Payload stored inside the JWT.
    Only the username is needed for authentication,
    but you can extend it with roles/permissions later.
    """
    sub: str = Field(..., description="Username or user id")
    exp: datetime | None = None


class TokenResponse(BaseModel):
    """
    Response returned by `/api/auth/token` and `/api/auth/register`.
    """
    access_token: str = Field(..., alias="access_token")
    token_type: str

    class Config:
        validate_by_name = True


class TokenData(BaseModel):
    username: Optional[str] = None
