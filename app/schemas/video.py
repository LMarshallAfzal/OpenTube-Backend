from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class VideoFormat(BaseModel):
    format_id: str
    format_note: Optional[str] = None
    ext: str
    vcodec: Optional[str] = None
    acodec: Optional[str] = None
    url: str
    width: Optional[int] = None
    height: Optional[int] = None
    fps: Optional[float] = None
    aspect_ratio: Optional[float] = None

    resolution: Optional[str] = None
    filesize_in_bytes: Optional[int] = None

    model_config = ConfigDict(
        extra="ignore"
    )


class VideoPublic(BaseModel):
    """Response model for video data"""
    id: str
    title: str
    thumbnail: Optional[str] = None
    duration_in_seconds: Optional[int] = None
    channel_id: Optional[str] = None
    channel_name: Optional[str] = None
    view_count: Optional[int] = None
    requested_by: Optional[str] = None
    formats: List[VideoFormat] | None = None
