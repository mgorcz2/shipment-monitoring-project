from uuid import uuid4

import pytest
from pydantic import ValidationError

from shipment_monitoring.core.domain.user import User, UserIn, UserRole


def test_userin_valid_data():
    data = {
        "email": "user@example.com",
        "password": "securepassword123",
        "role": "courier",
    }
    user = UserIn(**data)
    assert user.email == "user@example.com"
    assert user.role == UserRole.COURIER


def test_userin_min_password_length():
    user = UserIn(email="a@b.com", password="x")
    assert user.password == "x"


def test_userin_invalid_email():
    with pytest.raises(ValidationError):
        UserIn(email="invalid-email", password="password123")


def test_userin_invalid_role():
    with pytest.raises(ValidationError):
        UserIn(email="x@x.com", password="x", role="invalidrole")


def test_userin_default_role():
    user = UserIn(email="admin@domain.com", password="adminpass")
    assert user.role == UserRole.SENDER


def test_user_full_model():
    user = User(
        id=uuid4(),
        email="fulluser@domain.com",
        password="pass123",
        role=UserRole.SENDER,
    )
    assert isinstance(user.id, type(uuid4()))
    assert user.role == UserRole.SENDER


def test_userin_missing_password():
    with pytest.raises(ValidationError):
        UserIn(email="a@a.com")


def test_userin_missing_email():
    with pytest.raises(ValidationError):
        UserIn(password="abc123")
