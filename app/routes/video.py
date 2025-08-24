from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session
from pydantic import conint

from app.core.auth.dependencies import get_current_user
from app.db.session import get_session
from app.services.youtube import get_video_info, search_videos, first_thumbnail_url
from app.schemas.video import VideoPublic, VideoFormat

video_router = APIRouter(prefix="/api/video", tags=["Videos"])


@video_router.get("/{video_id}", response_model=VideoPublic)
async def get_video(
    video_id: str,
    # username: str = Depends(get_current_user),  # JWT protection
    db: Session = Depends(get_session)
):
    """Get streamable URL and metadata for a single video"""
    try:
        video_data = get_video_info(video_id)

        format_data = video_data["formats"]
        formats = []
        for fmt in format_data:
            if fmt.get("url").startswith("https://rr"):

                format = VideoFormat(
                    format_id=fmt.get("format_id"),
                    format_note=fmt.get("format_note"),
                    ext=fmt.get("ext"),
                    vcodec=fmt.get("vcodec"),
                    acodec=fmt.get("acodec"),
                    url=fmt.get("url"),
                    width=fmt.get("width"),
                    height=fmt.get("height"),
                    fps=fmt.get("fps"),
                    aspect_ratio=fmt.get("aspect_ratio"),
                    resolution=fmt.get("resolution"),
                    filesize_in_bytes=fmt.get("filesize_approx"),
                )

                formats.append(format)

        return VideoPublic(
            id=video_id,
            title=video_data["title"],
            thumbnail=first_thumbnail_url(video_data["thumbnail"]),
            duration_in_seconds=video_data["duration"],
            channel_id=video_data["channel_id"],
            channel_name=video_data["channel_name"],
            view_count=video_data["view_count"],
            formats=formats
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@video_router.get("/search/", response_model=List[VideoPublic])
async def search_youtube(
    query: str,
    max_results: conint(ge=1, le=50) = 5,
    db: Session = Depends(get_session)
):
    """Search YouTube videos"""
    if max_results <= 0 or max_results > 50:
        raise HTTPException(
            status_code=400, detail="max_results must be between 1 and 50")
    try:
        results, has_more = search_videos(query, max_results)

        return [
            VideoPublic(
                id=item["id"],
                title=item["title"],
                thumbnail=first_thumbnail_url(item["thumbnails"][0]),
                duration=item["duration"],
                channel_id=item["channel_id"],
                channel_name=item["channel_name"],
                view_count=item["view_count"]

            )
            for item in results
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
