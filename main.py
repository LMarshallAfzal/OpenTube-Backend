from fastapi import FastAPI
from sqlmodel import SQLModel

from routes import auth, video
from db.session import engine
from core.config import settings
from middleware.request_logger import log_request_body

app = FastAPI()

app.middleware("http")(log_request_body)

app.include_router(auth.router, prefix="/api/auth")
app.include_router(video.router, prefix="/api/videos", tags=["videos"])

# Initialise database (development only)
if settings.DB_DRIVER == "sqlite":
    @app.on_event("startup")
    def on_startup():
        SQLModel.metadata.create_all(bind=engine)
