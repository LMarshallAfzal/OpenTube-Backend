"""Base settings for the server"""
from pydantic_settings import BaseSettings
from pydantic import SecretStr
from sqlalchemy.engine.url import URL


class BaseAppSettings(BaseSettings):
    # Database settings
    DB_DRIVER: str = "sqlite"
    DB_HOST: str = ""
    DB_PORT: int = 0
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_NAME: str = "database.db"

    @property
    def DATABASE_URL(self) -> str:
        if self.DB_DRIVER == "sqlite":
            return f"sqlite:///{self.DB_NAME}"
        return str(URL.create(
            drivername="postgresql+psycopg2",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME
        ))

    # Authentication settings
    SECRET_KEY: SecretStr
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    SQLALCHEMY_ECHO: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


# Expose settings instance
settings = BaseAppSettings()
