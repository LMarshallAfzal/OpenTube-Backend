from fastapi import FastAPI
from routes import auth, video
from db.session import engine
from models.user import User


app = FastAPI()
app.include_router(auth.router, prefix="/api/auth")
# app.include_router(video.router, prefix="/api")

# Create DB TABLES (remove in production, use migrations)
User.metadata.create_all(bind=engine)
