import yt_dlp as youtube_dl
from typing import List, Dict


def get_video_info(video_id: str) -> Dict:
    """ Get streamable URL and metadata for a single video"""
    ydl_options = {
        "quiet": True,
        "no_warnings": True,
        "format": "best",
        "extract_flat": False,
    }
    with youtube_dl.YoutubeDL(ydl_options) as ydl:
        info = ydl.extract_info(f"https://youtu.be/{video_id}", download=False)
        return {
            "title": info.get("title", "No title"),
            "url": info["url"],
            "thumbnail": info.get("thumbnail", ""),
            "duration": info.get("duration"),
        }


def search_videos(query: str, max_results: int = 10) -> List[Dict]:
    """Search YouTube and return basic video info"""
    ydl_options = {
        "quiet": True,
        "extract_flat": True,
        "default_search": "ytsearch",
        "max_downloads": max_results,
    }
    with youtube_dl.YoutubeDL(ydl_options) as ydl:
        info = ydl.extract_info(f"ytsearch{max_results}:{
                                query}", download=False)
        return [
            {
                "id": entry["id"],
                "title": entry["title"],
                "thumbnails": [entry.get("thumbnail", "")],
                "duration": entry.get("duration"),
            }
            for entry in info["entries"]
        ]
