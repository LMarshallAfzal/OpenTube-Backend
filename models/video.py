from sqlmodel import SQLModel, Field
from typing import Optional


class VideoPublic(SQLModel):
    """Response model for video data"""
    id: str
    title: str
    stream_url: str
    thumbnail: str
    duration: Optional[int] = None
    requested_by: str
