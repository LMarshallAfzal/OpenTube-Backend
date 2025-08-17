from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import SQLModel

from app.routes.auth import auth_router
from app.routes.video import video_router
from app.db.session import engine
from app.core.settings.base import settings
from app.middleware.request_logger import log_request_body


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.DB_DRIVER == "sqlite":
        SQLModel.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="OpenTube", lifespan=lifespan)


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

# Routers
app.include_router(auth_router)
app.include_router(video_router)
