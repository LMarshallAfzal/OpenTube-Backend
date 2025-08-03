from sqlalchemy import create_engine
from core.config import settings


def create_db_engine():
    connect_args = {}
    if settings.DB_DRIVER == "sqlite":
        connect_args["check_same_thread"] = False

    return create_engine(
        settings.DATABASE_URL,
        connect_args=connect_args,
        echo=True,  # Turn off in production
    )


engine = create_db_engine()
