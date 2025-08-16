from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session

from app.core.auth.dependencies import get_current_user
from app.db.session import get_session
from app.services.youtube import get_video_info, search_videos
from app.models.video import VideoPublic

video_router = APIRouter()


@video_router.get("/{video_id}", response_model=VideoPublic)
async def get_video(
    video_id: str,
    username: str = Depends(get_current_user),  # JWT protection
    db: Session = Depends(get_session)
):
    """Get streamable URL and metadata for a single video"""
    try:
        video_data = get_video_info(video_id)
        return {
            "id": video_id,
            "title": video_data["title"],
            "stream_url": video_data["url"],
            "thumbnail": video_data["thumbnail"],
            "duration": video_data["duration"],
            "requested_by": username  # Track who requested this
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@video_router.get("/search/", response_model=List[VideoPublic])
async def search_youtube(
    query: str,
    max_results: int = 5,
    username: str = Depends(get_current_user),  # JWT protection
    db: Session = Depends(get_session)
):
    """Search YouTube videos"""
    try:
        results = search_videos(query, max_results)
        return [
            {
                "id": item["id"],
                "title": item["title"],
                "thumbnail": item["thumbnails"][0],
                "duration": item["duration"],
                "requested_by": username
            }
            for item in results
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
