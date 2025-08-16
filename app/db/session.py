""" FastAPI dependency that yields sqlModel.Session """
from typing import Generator
from sqlmodel import Session

from .engine import engine


def get_session() -> Generator[Session, None, None]:
    """
    Provide a session per request

    Yields
    ------
    Session
    A sqlmodel.Session bound to the application engine
    """
    with Session(engine) as session:
        yield session
