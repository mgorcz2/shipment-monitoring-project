import pytest

from shipment_monitoring.core.domain.user import UserIn
from shipment_monitoring.db import database, init_db
from shipment_monitoring.infrastructure.repositories.userdb import UserRepository


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
async def prepare_database():
    await init_db()
    await database.connect()
    yield
    await database.disconnect()


@pytest.mark.anyio
async def test_user_repository_crud():
    repo = UserRepository()
    assert await repo.get_user_by_email("alice@example.com") is None
    alice = UserIn(email="alice@example.com", password="pwd", role="sender")
    created = await repo.register_user(alice)
    assert created.email == "alice@example.com"
    fetched = await repo.get_user_by_email("alice@example.com")
    assert fetched.email == "alice@example.com"
