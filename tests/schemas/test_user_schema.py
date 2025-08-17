import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreate


def test_username_is_stripped():
    """Leading/trailing whitespace should be removed."""
    data = {"username": "   alice   ", "password": "validPass123"}
    user = UserCreate(**data)
    assert user.username == "alice"

    assert data["username"] == "   alice   "


def test_password_min_length():
    """Passwords shorter than 8 characters are rejected."""
    too_short = {"username": "bob", "password": "short"}
    with pytest.raises(ValidationError) as excinfo:
        UserCreate(**too_short)

    assert "should have at least 8 characters" in str(excinfo.value)


def test_valid_payload():
    """A perfectly fine payload passes."""
    data = {"username": "charlie", "password": "S3cur3Pass"}
    user = UserCreate(**data)
    assert user.username == "charlie"
    assert user.password == "S3cur3Pass"


def test_password_exactly_min_length():
    """8‑character password is accepted."""
    data = {"username": "dave", "password": "12345678"}
    user = UserCreate(**data)
    assert user.password == "12345678"


def test_missing_username_or_password():
    """Both fields are required – missing ones raise an error."""
    with pytest.raises(ValidationError) as excinfo:
        UserCreate(password="validPass")

    assert "username" in str(excinfo.value)

    with pytest.raises(ValidationError) as excinfo2:
        UserCreate(username="eve")

    assert "password" in str(excinfo2.value)


def test_password_as_none_or_empty():
    """None or an empty string is not allowed."""
    with pytest.raises(ValidationError):
        UserCreate(username="frank", password=None)

    with pytest.raises(ValidationError) as excinfo:
        UserCreate(username="grace", password="")
    print(str(excinfo.value))

    assert "should have at least 8 characters" in str(excinfo.value)
