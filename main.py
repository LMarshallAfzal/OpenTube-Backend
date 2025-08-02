from fastapi import FastAPI, HTTPException
import yt_dlp as youtube_dl
import httpx

app = FastAPI()


@app.get("/api/video")
async def get_video(video_id: str):
    """Fetch streamable URL for a Youtube video using yt-dlp"""
    try:
        youtube_dl_options = {
            "quiet": True,
            "no warnings": True,
            "format": "best",   # Auto-select best quality
        }
        with youtube_dl.YoutubeDL(youtube_dl_options) as ydl:
            info = ydl.extract_info(
                f"https://youtu.be/{video_id}", download=False)
            return {
                "title": info.get("title"),
                "stream_url": info["url"],  # Direct stream URL`
                "thumbnail": info.get("thumbnail"),
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
