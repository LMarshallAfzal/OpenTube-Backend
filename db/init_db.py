from sqlmodel import SQLModel, create_engine
from core.config import settings
from sqlalchemy import inspect
from models.user import User
from models.video import VideoPublic

engine = create_engine(settings.DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)  # Creates tables from models
    inspector = inspect(engine)
    print("Created tables:", list(inspector.get_table_names()))


if __name__ == "__main__":
    init_db()
