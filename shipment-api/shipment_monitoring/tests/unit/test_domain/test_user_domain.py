from uuid import uuid4

import pytest
from pydantic import ValidationError

from shipment_monitoring.core.domain.user import User, UserIn, UserRole, UserUpdate


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
    with pytest.raises(
        ValidationError, match="String should have at least 8 characters"
    ):
        UserIn(email=valid_email, password="Abcdef7")


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
    with pytest.raises(
        ValidationError, match="String should have at most 128 characters"
    ):
        UserIn(email=valid_email, password="a" * 129)


def test_userin_password_missing_uppercase(valid_email):
    with pytest.raises(
        ValidationError, match="Password must contain at least one uppercase letter"
    ):
        UserIn(email=valid_email, password="abcd1234!")


def test_userin_password_missing_special_or_number(valid_email):
    with pytest.raises(
        ValidationError,
        match="Password must contain at least one number or special character",
    ):
        UserIn(email=valid_email, password="Abcdefgh")


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


def test_user_update_empty():
    update = UserUpdate()
    assert update.email is None
    assert update.password is None
    assert update.role is None


def test_user_update_partial_email(valid_email):
    update = UserUpdate(email=valid_email)
    assert update.email == valid_email
    assert update.password is None
    assert update.role is None


def test_user_update_partial_password(valid_password):
    update = UserUpdate(password=valid_password)
    assert update.email is None
    assert update.password == valid_password
    assert update.role is None


def test_user_update_partial_role():
    update = UserUpdate(role=UserRole.ADMIN)
    assert update.email is None
    assert update.password is None
    assert update.role == UserRole.ADMIN


def test_user_update_all_fields(valid_email, valid_password):
    update = UserUpdate(
        email=valid_email, password=valid_password, role=UserRole.COURIER.value
    )
    assert update.email == valid_email
    assert update.password == valid_password
    assert update.role == UserRole.COURIER
