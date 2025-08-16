from __future__ import annotations

from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(sa_column_kwargs={"unique": True})
    hashed_password: str

    # history: List["History"] = Relationship(back_populates="user")
