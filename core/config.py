from pathlib import Path
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / ".env")


class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/database.db"

    class Config:
        env_file = ".env"


# Initialise after class definition
settings = Settings()
