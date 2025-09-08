from uuid import uuid4

# pylint: disable=redefined-outer-name
import pytest

from shipment_monitoring.core.domain.user import User, UserIn, UserUpdate
from shipment_monitoring.infrastructure.dto.userDTO import UserDTO


@pytest.fixture(scope="session")
def anyio_backend():
    """
    Specify the backend to use for anyio tests.
    This is necessary for compatibility with pytest-asyncio.
    """
    return "asyncio"


@pytest.fixture
def valid_password():
    return "Securepassword123!"


@pytest.fixture
def valid_email():
    return "validemail@example.com"


@pytest.fixture
def valid_userin(valid_email, valid_password):
    return UserIn(
        email=valid_email,
        password=valid_password,
        role="sender",
    )


@pytest.fixture
def valid_user(valid_email, valid_password):
    return User(
        id=uuid4(),
        email=valid_email,
        password=valid_password,
        role="sender",
    )


@pytest.fixture
def valid_userDTO(valid_email):
    return UserDTO(
        id=uuid4(),
        email=valid_email,
        role="sender",
    )


@pytest.fixture
def valid_user_update(valid_email, valid_password):
    return UserUpdate(
        email=valid_email,
        password=valid_password,
        role="sender",
    )
