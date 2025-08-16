import pytest
from sqlmodel import Session, create_engine, select
from app.models import User            # your model


@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")
    User.metadata.create_all(engine)
    with Session(engine) as sess:
        yield sess
    User.metadata.drop_all(engine)


def test_user_creation(session):
    u = User(username="alice", hashed_password="pw123")
    session.add(u)
    session.commit()
    assert u.id is not None


def test_unique_username(session):
    session.add(User(username="bob", hashed_password="pw1"))
    session.commit()

    dup = User(username="bob", hashed_password="pw2")
    session.add(dup)

    with pytest.raises(Exception) as exc:
        session.commit()
    assert "UNIQUE constraint failed" in str(exc.value)


def test_query_by_username(session):
    session.add_all([
        User(username="eve", hashed_password="a"),
        User(username="mallory", hashed_password="b")
    ])
    session.commit()

    stmt = select(User).where(User.username == "eve")
    user = session.exec(stmt).first()
    assert user is not None
    assert user.username == "eve"
