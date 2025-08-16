import pytest
from sqlmodel import Session, create_engine, select
from fastapi import HTTPException

from app.services.auth import create_user, authenticate_user
from app.models.user import User


@pytest.fixture(scope="function")
def session():
    """
    Return a fresh in-memory database and a SQLModel Session.
    """
    engine = create_engine("sqlite:///:memory:")
    User.metadata.create_all(engine)

    with Session(engine) as sess:
        yield sess

    User.metadata.drop_all


def test_create_user_success(session):
    """A new user is added and returned with and id."""
    user = create_user(session, "alice", "secret")
    assert user.id is not None
    assert user.username == "alice"

    db_user = session.exec(select(User).where(
        User.username == "alice")).first()
    assert db_user is not None
