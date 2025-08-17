# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, SQLModel, Session
from app.main import app
from app.db.session import get_session
from app.models.user import User


@pytest.fixture(scope="module")
def db_engine():
    # A shared in‑memory database that survives for the whole test module.
    engine = create_engine(
        "sqlite:///:memory:?cache=shared",
        connect_args={"check_same_thread": False},
        echo=False,
    )
    SQLModel.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="module")
def override_session(db_engine):
    # This fixture must run **before** the client is created.
    def _session():
        with Session(db_engine) as session:
            yield session
    app.dependency_overrides[get_session] = _session
    import app.db.session as db_sess
    db_sess.engine = db_engine


@pytest.fixture(scope="module")
def client(override_session):
    # The client will now use the overridden dependency.
    with TestClient(app) as c:
        yield c
