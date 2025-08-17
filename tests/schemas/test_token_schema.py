import pytest
from datetime import datetime, timezone, timedelta
from pydantic import ValidationError

from app.schemas.token import TokenPayload, TokenResponse, TokenData


def test_token_payload_required_sub():
    """`sub` must be present."""
    with pytest.raises(ValidationError) as excinfo:
        TokenPayload()

    assert "field required" in str(excinfo.value).lower()
    assert "sub" in str(excinfo.value).lower()


def test_token_payload_exp_optional_and_parsed():
    """`exp` can be omitted or supplied as a datetime."""
    payload = TokenPayload(sub="alice")
    assert payload.sub == "alice"
    assert payload.exp is None

    future = datetime.now(timezone.utc) + timedelta(days=1)
    payload2 = TokenPayload(sub="bob", exp=future)
    assert payload2.exp == future

    iso_str = "2025-12-31T23:59:59Z"
    payload3 = TokenPayload(sub="carol", exp=iso_str)
    assert isinstance(payload3.exp, datetime)


def test_token_response_alias_and_validation():
    """`access_token` is an alias; `token_type` must be supplied."""
    data = {"access_token": "sometoken", "token_type": "bearer"}
    resp = TokenResponse(**data)

    assert resp.access_token == "sometoken"
    assert resp.token_type == "bearer"

    data2 = {"accessToken": "bad", "token_type": "bearer"}
    with pytest.raises(ValidationError) as excinfo:
        TokenResponse(**data2)

    assert "access_token" in str(excinfo.value).lower()


def test_token_response_validate_by_name():
    """`validate_by_name=True` means the attribute name is used for validation."""
    data = {"accessToken": "oops", "token_type": "bearer"}
    with pytest.raises(ValidationError) as excinfo:
        TokenResponse(**data)

    assert "access_token" in str(excinfo.value).lower()


def test_token_data_optional_username():
    """`username` is optional and defaults to None."""
    td = TokenData()
    assert td.username is None

    td2 = TokenData(username="alice")
    assert td2.username == "alice"

    td3 = TokenData(username="")
    assert td3.username == ""


def test_token_payload_round_trip():
    """Model can be parsed from dict and exported back."""
    data = {"sub": "bob", "exp": datetime.now(timezone.utc)}
    payload = TokenPayload(**data)
    out_dict = payload.model_dump(mode="json")
    assert out_dict["sub"] == "bob"
    assert isinstance(out_dict["exp"], str)


def test_token_response_round_trip():
    resp = TokenResponse(access_token="abc123", token_type="bearer")
    out = resp.model_dump(by_alias=True)
    assert "access_token" in out
    assert out["token_type"] == "bearer"
