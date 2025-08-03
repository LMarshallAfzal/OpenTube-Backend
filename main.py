from fastapi import FastAPI
from sqlmodel import SQLModel
from routes import auth, video
from db.session import engine
from models.user import User
from models.video import VideoPublic


app = FastAPI()
app.include_router(auth.router, prefix="/api/auth")
app.include_router(video.router)

# Create DB TABLES (remove in production, use migrations)
SQLModel.metadata.create_all(bind=engine)
