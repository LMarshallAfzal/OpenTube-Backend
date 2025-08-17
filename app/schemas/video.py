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
    stream_url: str
    thumbnail: Optional[str] = None
    duration: Optional[int] = None
    formats: List[VideoFormat]
    requested_by: Optional[str] = None
