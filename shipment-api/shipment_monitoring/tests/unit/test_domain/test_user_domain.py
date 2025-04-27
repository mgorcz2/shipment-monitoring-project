from uuid import uuid4

import pytest
from pydantic import ValidationError

from shipment_monitoring.core.domain.user import User, UserIn, UserRole


def test_userin_valid_data(valid_password, valid_email):
    data = {
        "email": valid_email,
        "password": valid_password,
        "role": "courier",
    }
    user = UserIn(**data)
    assert user.email == valid_email
    assert user.role == UserRole.COURIER
    assert user.password == valid_password


def test_userin_password_too_short(valid_email):  # left neighbor value
    with pytest.raises(ValidationError) as exc_info:
        UserIn(email=valid_email, password="Abcdef7")
    assert "String should have at least 8 characters" in str(exc_info.value)


def test_userin_password_exact_minimum_lenght(valid_email):  # right neighbor value
    user = UserIn(email=valid_email, password="Abcdefgh9")
    assert len(user.password) == 9


def test_userin_password_exact_maximum_lenght(valid_email):  # left neighbor value
    user = UserIn(email=valid_email, password="A" * 126 + "1")
    assert len(user.password) == 127


def test_userin_password_maximum_lenght(valid_email):
    user = UserIn(email=valid_email, password="A" * 127 + "1")  # boundary value
    assert len(user.password) == 128


def test_userin_password_too_long(valid_email):  # right neighbor value
    with pytest.raises(ValidationError) as exc_info:
        UserIn(email=valid_email, password="a" * 129)
    assert "String should have at most 128 characters" in str(exc_info.value)


def test_userin_password_missing_uppercase(valid_email):
    with pytest.raises(ValidationError) as exc_info:
        UserIn(email=valid_email, password="abcd1234!")
    assert "Password must contain at least one uppercase letter" in str(exc_info.value)


def test_userin_password_missing_special_or_number(valid_email):
    with pytest.raises(ValidationError) as exc_info:
        UserIn(email=valid_email, password="Abcdefgh")
    assert "Password must contain at least one number or special character" in str(
        exc_info.value
    )


@pytest.mark.parametrize(
    "email",
    [
        "user@example.com",
        "valid.email@domain.co.uk",
        "user123@subdomain.domain.com",
        "user+special@domain.com",
    ],
)
def test_valid_email(email, valid_password):
    """Test valid email addresses."""
    user = UserIn(email=email, password=valid_password)
    assert user.email == email


@pytest.mark.parametrize(
    "email",
    [
        "invalid-email",
        "user@domain",
        "@domain.com",
        "user@domain,com",
    ],
)
def test_invalid_email(email, valid_password):
    """Test invalid email addresses."""
    with pytest.raises(ValidationError):
        UserIn(email=email, password=valid_password)


def test_userin_invalid_role(valid_email, valid_password):
    with pytest.raises(ValidationError):
        UserIn(email=valid_email, password=valid_password, role="invalidrole")
    with pytest.raises(ValidationError):
        UserIn(email=valid_email, password=valid_password, role="")


def test_userin_default_role(valid_email, valid_password):
    user = UserIn(email=valid_email, password=valid_password)
    assert user.role == UserRole.SENDER


def test_userin_missing_password(valid_email):
    with pytest.raises(ValidationError):
        UserIn(email=valid_email, password=None)


def test_userin_empty_password(valid_email):
    with pytest.raises(ValidationError):
        UserIn(email=valid_email, password="")


def test_userin_missing_email(valid_password):
    with pytest.raises(ValidationError):
        UserIn(email=None, password=valid_password)


def test_userin_empty_email(valid_password):
    with pytest.raises(ValidationError):
        UserIn(email="", password=valid_password)


def test_user_model(valid_email, valid_password):
    user = User(
        id=uuid4(),
        email=valid_email,
        password=valid_password,
        role=UserRole.SENDER,
    )
    assert isinstance(user.id, type(uuid4()))
    assert user.email == valid_email
    assert user.password == valid_password
    assert user.role == UserRole.SENDER
