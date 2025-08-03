from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import SecretStr
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent

# Load environment variables from .env file


class Settings(BaseSettings):
    SECRET_KEY: SecretStr
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/database.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


# Initialise after class definition
settings = Settings()
