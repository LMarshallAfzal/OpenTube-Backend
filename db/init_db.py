from sqlmodel import SQLModel, create_engine
from core.config import settings
from models.user import User

engine = create_engine(settings.DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)  # Creates tables from models


if __name__ == "__main__":
    init_db()
