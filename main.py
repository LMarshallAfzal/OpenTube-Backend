from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from routes import auth_router, video
from db.session import engine
from core.settings.base import settings
from middleware.request_logger import log_request_body

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
app.include_router(video.router, prefix="/api/videos", tags=["videos"])

# Initialise database (development only)
if settings.DB_DRIVER == "sqlite":
    @app.on_event("startup")
    def on_startup():
        SQLModel.metadata.create_all(bind=engine)
