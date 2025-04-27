import uuid

import pytest

from shipment_monitoring.core.domain.user import User, UserIn, UserRole

users_data = [
    ("test1@example.com", "Password123", UserRole.SENDER),
    ("another.user@example.org", "AnotherPass321", UserRole.COURIER),
    ("user+special@example.com", "SpecialPass!@#", UserRole.ADMIN),
]


@pytest.mark.anyio
async def test_register_user(user_repository, valid_userin):
    created = await user_repository.register_user(valid_userin)
    assert created.email == valid_userin.email


@pytest.mark.anyio
async def test_get_user_by_email(user_repository, valid_userin):
    await user_repository.register_user(valid_userin)
    fetched = await user_repository.get_user_by_email(valid_userin.email)
    assert fetched["email"] == valid_userin.email


@pytest.mark.anyio
async def test_get_user_by_id(user_repository, valid_userin):
    created = await user_repository.register_user(valid_userin)
    fetched = await user_repository.get_user_by_id(created.id)
    assert fetched["id"] == created.id


@pytest.mark.anyio
async def test_delete_user(user_repository, valid_userin):
    await user_repository.register_user(valid_userin)
    deleted = await user_repository.detele_user(valid_userin.email)
    assert deleted["email"] == valid_userin.email
    assert await user_repository.get_user_by_email(valid_userin.email) is None


@pytest.mark.anyio
async def test_update_user(user_repository, valid_userin):
    created = await user_repository.register_user(valid_userin)
    new_data = User(
        id=created.id,
        email="new@example.com",
        password=created.password,
        role=created.role,
    )
    updated = await user_repository.update_user(valid_userin.email, new_data)
    assert updated["email"] == "new@example.com"


@pytest.mark.anyio
async def test_get_all_users(user_repository, valid_userin):
    await user_repository.register_user(valid_userin)
    users = await user_repository.get_all_users()
    assert isinstance(users, list)
    assert any(u["email"] == valid_userin.email for u in users)


@pytest.mark.parametrize("email,password,role", users_data)
@pytest.mark.anyio
async def test_register_multiple_users(user_repository, email, password, role):
    user_in = UserIn(email=email, password=password, role=role)
    created = await user_repository.register_user(user_in)
    assert created.email == email
    fetched = await user_repository.get_user_by_email(email)
    assert fetched["email"] == email


@pytest.mark.parametrize("email,password,role", users_data)
@pytest.mark.anyio
async def test_get_users_by_role(user_repository, email, password, role):
    user_in = UserIn(email=email, password=password, role=role)
    await user_repository.register_user(user_in)
    fetched = await user_repository.get_users_by_role(role)
    assert isinstance(fetched, list)
    assert len(fetched) == 1


@pytest.mark.anyio
async def test_register_duplicate_user(user_repository, valid_userin):
    await user_repository.register_user(valid_userin)
    with pytest.raises(Exception):
        await user_repository.register_user(valid_userin)


@pytest.mark.anyio
async def test_delete_nonexistent_user(user_repository):
    deleted = await user_repository.detele_user("nonexistent@example.com")
    assert deleted is None


@pytest.mark.anyio
async def test_update_nonexistent_user(user_repository):
    non_existing_email = "notfound@example.com"
    fake_user = User(
        id=str(uuid.uuid4()),
        email="new@example.com",
        password="Newpass123",
        role=UserRole.COURIER,
    )
    updated = await user_repository.update_user(non_existing_email, fake_user)
    assert updated is None


@pytest.mark.anyio
async def test_get_all_users_empty(user_repository):
    users = await user_repository.get_all_users()
    assert users == []
