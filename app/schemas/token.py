from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


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

    model_config = ConfigDict(
        validate_by_name=True,
        populate_by_alias=True,
    )

    # class Config:
    #     validate_by_name = True


class TokenData(BaseModel):
    username: Optional[str] = None
