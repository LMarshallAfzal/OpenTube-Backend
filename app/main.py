from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from app.routes.auth import auth_router
from app.routes.video import video_router
from app.db.session import engine
from app.core.settings.base import settings
from app.middleware.request_logger import log_request_body

app = FastAPI(title="OpenTube")

app.middleware("http")(log_request_body)

origins = [
    "http://localhost:8000",
]

# Change these in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(video_router, prefix="/api/videos", tags=["videos"])

# Initialise database (development only)
if settings.DB_DRIVER == "sqlite":
    @app.on_event("startup")
    def on_startup():
        SQLModel.metadata.create_all(bind=engine)
