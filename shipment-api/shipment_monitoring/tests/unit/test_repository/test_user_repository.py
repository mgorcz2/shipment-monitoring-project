from uuid import UUID, uuid4

import pytest

import shipment_monitoring.infrastructure.repositories.userdb as repo_module
from shipment_monitoring.core.domain.user import User, UserIn, UserRole
from shipment_monitoring.infrastructure.repositories.userdb import UserRepository


@pytest.fixture(autouse=True)
def patch_database(mocker, valid_user):
    db = mocker.patch.object(repo_module, "database")
    db.execute = mocker.AsyncMock(return_value=valid_user.id)
    db.fetch_one = mocker.AsyncMock(return_value=valid_user)
    db.fetch_all = mocker.AsyncMock(return_value=[valid_user])
    return db


@pytest.fixture
def repository():
    return UserRepository()


@pytest.mark.anyio
async def test_register_user(repository, patch_database, valid_userin, valid_user):
    result = await repository.register_user(valid_userin)
    assert isinstance(result, User)
    assert result.id == valid_user.id
    patch_database.execute.assert_awaited()
    patch_database.fetch_one.assert_awaited()


@pytest.mark.anyio
async def test_register_user_returns_none(repository, patch_database, valid_userin):
    patch_database.execute.return_value = None
    patch_database.fetch_one.return_value = None
    result = await repository.register_user(valid_userin)
    assert result is None
    patch_database.execute.assert_awaited_once()


@pytest.mark.anyio
async def test_get_user_by_id(repository, patch_database, valid_user):
    result = await repository.get_user_by_id(valid_user.id)
    assert result == valid_user
    patch_database.fetch_one.assert_awaited_once()


@pytest.mark.anyio
async def test_get_user_returns_none(repository, patch_database, valid_user):
    patch_database.fetch_one.return_value = None
    result = await repository.get_user_by_id(valid_user.id)
    assert result is None
    patch_database.fetch_one.assert_awaited_once()


@pytest.mark.anyio
async def test_get_user_by_email(repository, patch_database, valid_user):
    result = await repository.get_user_by_email(valid_user.email)
    assert result == valid_user
    patch_database.fetch_one.assert_awaited_once()


@pytest.mark.anyio
async def test_get_user_by_email_returns_none(repository, patch_database, valid_user):
    patch_database.fetch_one.return_value = None
    result = await repository.get_user_by_email(valid_user.email)
    assert result is None
    patch_database.fetch_one.assert_awaited_once()


@pytest.mark.anyio
async def test_delete_user(repository, patch_database, valid_user):
    result = await repository.detele_user(valid_user.email)
    assert result == valid_user
    patch_database.fetch_one.assert_awaited_once()


@pytest.mark.anyio
async def test_delete_user_returns_none(repository, patch_database, valid_user):
    patch_database.fetch_one.return_value = None
    result = await repository.detele_user(valid_user.email)
    assert result is None
    patch_database.fetch_one.assert_awaited_once()


@pytest.mark.anyio
async def test_update_user(repository, patch_database, valid_user):
    patch_database.fetch_one.return_value = valid_user
    data = UserIn(
        email=valid_user.email, password=valid_user.password, role=valid_user.role
    )
    result = await repository.update_user(valid_user.email, data)
    assert result == valid_user
    patch_database.fetch_one.assert_awaited_once()


@pytest.mark.anyio
async def test_update_user_returns_none(repository, patch_database, valid_user):
    patch_database.fetch_one.return_value = None
    data = UserIn(
        email=valid_user.email, password=valid_user.password, role=valid_user.role
    )
    result = await repository.update_user(valid_user.email, data)
    assert result is None
    patch_database.fetch_one.assert_awaited_once()


@pytest.mark.anyio
async def test_get_all_users(repository, patch_database, valid_user):
    result = await repository.get_all_users()
    assert isinstance(result, list)
    assert result[0] == valid_user
    patch_database.fetch_all.assert_awaited_once()


@pytest.mark.anyio
async def test_get_all_users_empty(repository, patch_database):
    patch_database.fetch_all.return_value = []
    result = await repository.get_all_users()
    assert isinstance(result, list)
    assert len(result) == 0
    assert result == []
    patch_database.fetch_all.assert_awaited_once()


@pytest.mark.parametrize(
    "user",
    [
        User(
            id=uuid4(),
            email="user@example.com",
            password="Password123",
            role="sender",
        ),
        User(
            id=uuid4(),
            email="user@example.com",
            password="Password123",
            role="admin",
        ),
        User(
            id=uuid4(),
            email="user@example.com",
            password="Password123",
            role="courier",
        ),
        User(
            id=uuid4(),
            email="user@example.com",
            password="Password123",
            role="manager",
        ),
    ],
)
@pytest.mark.anyio
async def test_get_users_by_role(
    repository,
    patch_database,
    user,
):
    patch_database.fetch_all.return_value = [user]
    result = await repository.get_users_by_role(user.role)
    assert isinstance(result, list)
    assert user in result
    patch_database.fetch_all.assert_awaited_once()
