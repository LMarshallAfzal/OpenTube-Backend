from sqlmodel import SQLModel, Field
from typing import Optional


class VideoPublic(SQLModel, table=True):
    """Response model for video data"""
    id: str = Field(primary_key=True)
    title: str
    stream_url: str
    thumbnail: str
    duration: Optional[int] = None
    requested_by: str
