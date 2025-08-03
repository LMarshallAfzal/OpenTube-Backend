from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from models.user import User


class HistoryBase(SQLModel):
    user_id: int = Field(foreign_key="user.id", index=True)
    video_id: str
    watched_at: datetime = Field(default_facotry=datetime.utcnow)
    progress_seconds: Optional[int] = Field(default=0, ge=0)


class History(HistoryBase, table=True):
    id: UUID = Field(
        dfault_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False
    )

    # Relationship to User
    user: Optional["User"] = Relationship(back_populates="history")


class HistoryCreate(HistoryBase):
    pass


class HistoryREad(HistoryBase):
    id: UUID
