import yt_dlp as youtube_dl
from typing import List, Dict, Tuple
from fastapi import HTTPException


def get_video_info(video_id: str) -> Dict:
    """ Get streamable URL and metadata for a single video"""
    ydl_options = {
        "quiet": True,
        "no_warnings": True,
        "format": "bestvideo+bestaudio/best",
        "extract_flat": False,
    }
    with youtube_dl.YoutubeDL(ydl_options) as ydl:
        info = ydl.extract_info(f"https://youtu.be/{video_id}", download=False)
        return {
            "title": info.get("title", "No title"),
            "url": info.get("url"),
            "thumbnail": info.get("thumbnails", ""),
            "duration": info.get("duration"),
            "formats": info.get("formats", []),
            "channel_id": info.get("channel_id"),
            "channel_name": info.get("channel_name"),
            "view_count": info.get("view_count")
        }


def search_videos(query: str, limit: int) -> Tuple[List[Dict], bool]:
    """Search YouTube and return basic video info"""
    ydl_options = {
        "quiet": True,
        "extract_flat": True,
        "default_search": "ytsearch",
        "skip_download": True,
        "noplaylist": True,
    }

    with youtube_dl.YoutubeDL(ydl_options) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch{limit + 1}:{
                query}", download=False)
        except youtube_dl.utils.DownloadError as exc:
            raise HTTPException(status_code=502, detail=str(exc))

        entries = info.get("entries", [])
        has_more = len(entries) > limit
        entries = entries[:limit]

        return [
            {
                "id": entry["id"],
                "title": entry["title"],
                "url": entry["url"],
                "description": entry["description"],
                "thumbnails": [entry.get("thumbnails", "")],
                "duration": entry.get("duration"),
                "channel_id": entry.get("channel_id"),
                "channel_name": entry.get("channel"),
                "view_count": entry.get("view_count")
            }
            for entry in entries
        ], has_more


def first_thumbnail_url(thumbnails: List[Dict]) -> str | None:
    """Return the URL of the first thumbnail or None if missing."""
    return thumbnails[0]["url"] if thumbnails else None
