"""Unit tests for User repository."""

# pylint: disable=redefined-outer-name
from uuid import uuid4

import pytest

import src.infrastructure.repositories.userdb as repo_module
from src.core.domain.user import User, UserIn
from src.infrastructure.repositories.userdb import UserRepository


@pytest.fixture(autouse=True)
def patch_database(mocker, valid_user):
    """
    Patch the database connection and its methods to avoid actual database calls.
    """
    db = mocker.patch.object(repo_module, "database")
    db.execute = mocker.AsyncMock(return_value=valid_user.id)
    db.fetch_one = mocker.AsyncMock(return_value=valid_user)
    db.fetch_all = mocker.AsyncMock(return_value=[valid_user])
    return db


@pytest.fixture
def repository():
    """
    Fixture to provide a UserRepository instance for testing.
    """
    return UserRepository()


@pytest.mark.anyio
async def test_register_user(repository, patch_database, valid_userin, valid_user):
    """
    Test the register_user method of the UserRepository.
    """
    result = await repository.register_user(valid_userin)
    assert isinstance(result, User)
    assert result.id == valid_user.id
    patch_database.execute.assert_awaited()
    patch_database.fetch_one.assert_awaited()


@pytest.mark.anyio
async def test_register_user_returns_none(repository, patch_database, valid_userin):
    """
    Test the register_user method of the UserRepository when it returns None.
    """
    patch_database.execute.return_value = None
    patch_database.fetch_one.return_value = None
    result = await repository.register_user(valid_userin)
    assert result is None
    patch_database.execute.assert_awaited_once()


@pytest.mark.anyio
async def test_get_user_by_id(repository, patch_database, valid_user):
    """
    Test the get_user_by_id method of the UserRepository.
    """
    result = await repository.get_user_by_id(valid_user.id)
    assert result == valid_user
    patch_database.fetch_one.assert_awaited_once()


@pytest.mark.anyio
async def test_get_user_returns_none(repository, patch_database, valid_user):
    """
    Test the get_user_by_id method of the UserRepository when it returns None.
    """
    patch_database.fetch_one.return_value = None
    result = await repository.get_user_by_id(valid_user.id)
    assert result is None
    patch_database.fetch_one.assert_awaited_once()


@pytest.mark.anyio
async def test_get_user_by_email(repository, patch_database, valid_user):
    """
    Test the get_user_by_email method of the UserRepository.
    """
    result = await repository.get_user_by_email(valid_user.email)
    assert result == valid_user
    patch_database.fetch_one.assert_awaited_once()


@pytest.mark.anyio
async def test_get_user_by_email_returns_none(repository, patch_database, valid_user):
    """
    Test the get_user_by_email method of the UserRepository when it returns None.
    """
    patch_database.fetch_one.return_value = None
    result = await repository.get_user_by_email(valid_user.email)
    assert result is None
    patch_database.fetch_one.assert_awaited_once()


@pytest.mark.anyio
async def test_delete_user(repository, patch_database, valid_user):
    """
    Test the delete_user method of the UserRepository.
    """
    result = await repository.detele_user(valid_user.email)
    assert result == valid_user
    patch_database.fetch_one.assert_awaited_once()


@pytest.mark.anyio
async def test_delete_user_returns_none(repository, patch_database, valid_user):
    """
    Test the delete_user method of the UserRepository when it returns None.
    """
    patch_database.fetch_one.return_value = None
    result = await repository.detele_user(valid_user.email)
    assert result is None
    patch_database.fetch_one.assert_awaited_once()


@pytest.mark.anyio
async def test_update_user(repository, patch_database, valid_user):
    """
    Test the update_user method of the UserRepository.
    """
    patch_database.fetch_one.return_value = valid_user
    data = UserIn(
        email=valid_user.email, password=valid_user.password, role=valid_user.role
    )
    result = await repository.update_user(valid_user.email, data)
    assert result == valid_user
    patch_database.fetch_one.assert_awaited_once()


@pytest.mark.anyio
async def test_update_user_returns_none(repository, patch_database, valid_user):
    """
    Test the update_user method of the UserRepository when it returns None.
    """
    patch_database.fetch_one.return_value = None
    data = UserIn(
        email=valid_user.email, password=valid_user.password, role=valid_user.role
    )
    result = await repository.update_user(valid_user.email, data)
    assert result is None
    patch_database.fetch_one.assert_awaited_once()


@pytest.mark.anyio
async def test_get_all_users(repository, patch_database, valid_user):
    """
    Test the get_all_users method of the UserRepository.
    """
    result = await repository.get_all_users()
    assert isinstance(result, list)
    assert result[0] == valid_user
    patch_database.fetch_all.assert_awaited_once()


@pytest.mark.anyio
async def test_get_all_users_empty(repository, patch_database):
    """
    Test the get_all_users method of the UserRepository when it returns an empty list.
    """
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
    """
    Test the get_users_by_role method of the UserRepository.
    """
    patch_database.fetch_all.return_value = [user]
    result = await repository.get_users_by_role(user.role)
    assert isinstance(result, list)
    assert user in result
    patch_database.fetch_all.assert_awaited_once()
