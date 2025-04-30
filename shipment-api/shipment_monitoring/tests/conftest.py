from uuid import uuid4

import pytest

from shipment_monitoring.core.domain.user import User, UserIn
from shipment_monitoring.db import database, init_db
from shipment_monitoring.infrastructure.repositories.userdb import UserRepository


@pytest.fixture(scope="session")
def anyio_backend():
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
