from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, select

from app.main import app
from app.db.session import get_session
from app.models.user import User


def print_table_names(engine):
    """Print every table that SQLModel thinks has been created."""
    # 1️⃣ The metadata object keeps a mapping of name → Table
    for tablename in SQLModel.metadata.tables:
        print(f"Metadata knows about: {tablename}")

    # 2️⃣ Ask the engine itself (works with SQLite, PostgreSQL, …)
    #   `engine.table_names()` is deprecated; use `inspect`.
    from sqlalchemy import inspect
    inspector = inspect(engine)
    print("Engine reports tables:", inspector.get_table_names())


def test_register_success(client: TestClient, db_engine):
    """A fresh user can sign up and receives a token."""
    payload = {"username": "alice", "password": "StrongPass123"}
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)

    with Session(db_engine) as sess:
        result = sess.exec(
            select(User).where(User.username == "alice")
        ).first()
        assert result is not None


def test_login_success(client: TestClient):
    """Login with correct credentials returns a token."""
    # First create the user via the same register endpoint
    client.post("/api/auth/register",
                json={"username": "bob", "password": "MySecret456"})

    # OAuth2PasswordRequestForm expects form‑encoded data
    login_payload = {"username": "bob", "password": "MySecret456"}
    response = client.post("/api/auth/token", data=login_payload)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)


def test_login_wrong_password(client: TestClient):
    """Wrong password → 401 with the correct WWW-Authenticate header."""
    # Ensure user exists
    client.post("/api/auth/register",
                json={"username": "carol", "password": "RightPassword"})

    login_payload = {"username": "carol", "password": "WrongPass"}
    response = client.post("/api/auth/token", data=login_payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect username or password"
    # Header set by the route
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_login_nonexistent_user(client: TestClient):
    """If the user does not exist, we also get 401."""
    login_payload = {"username": "doesnotexist", "password": "nopass"}
    response = client.post("/api/auth/token", data=login_payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect username or password"
