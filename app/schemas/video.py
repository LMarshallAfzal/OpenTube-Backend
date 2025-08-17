from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class VideoFormat(BaseModel):
    format_id: str
    ext: str
    resolution: Optional[str] = None

    filesize: Optional[int] = None
    vcodec: Optional[str] = None
    acodec: Optional[str] = None

    url: str

    model_config = ConfigDict(
        extra="ignore"
    )


class VideoPublic(BaseModel):
    """Response model for video data"""
    id: str
    title: str
    stream_url: Optional[str] = None
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    duration: Optional[int] = None
    formats: List[VideoFormat] | None = None
    channel_id: Optional[str] = None
    channel_name: Optional[str] = None
    view_count: Optional[int] = None
    requested_by: Optional[str] = None
