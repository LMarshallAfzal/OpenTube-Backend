from sqlmodel import create_engine, Session
from core.config import settings


engine = create_engine(settings.DATABASE_URL, echo=True)  # Add to config.py


def get_db():
    with Session(engine) as session:
        yield session
