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
        User.username == "alice"))
    assert db_user is not None


def test_create_user_duplicate_username(session):
    """Creating a user with an existing username raises HTTPException."""
    create_user(session, "bob", "pw1")  # first one succeeds

    with pytest.raises(HTTPException) as exc:
        create_user(session, "bob", "pw2")

    assert exc.value.status_code == 400
    assert exc.value.detail == "Username already registered"

    # Verify that only the *first* user exists
    users = session.exec(select(User).where(User.username == "bob")).all()
    assert len(users) == 1


def test_authenticate_success(session):
    """Correct credentials return a User instance."""
    create_user(session, "eve", "mypassword")

    user = authenticate_user(session, "eve", "mypassword")
    assert user is not None
    assert user.username == "eve"


def test_authenticate_wrong_password(session):
    """Wrong password returns ``None``."""
    create_user(session, "mallory", "goodpw")

    result = authenticate_user(session, "mallory", "badpw")
    assert result is None


def test_authenticate_nonexistent_user(session):
    """Unknown username returns ``None``."""
    result = authenticate_user(session, "ghost", "doesntmatter")
    assert result is None
