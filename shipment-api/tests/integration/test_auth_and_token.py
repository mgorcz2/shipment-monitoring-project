"""Integration tests for user authentication and authorization in the shipment monitoring system."""

# pylint: disable=redefined-outer-name
from datetime import datetime, timedelta, timezone

import pytest
from freezegun import freeze_time
from httpx import ASGITransport, AsyncClient
from src.core.domain.user import UserRole
from src.core.security.consts import ACCESS_TOKEN_EXPIRE_MINUTES
from src.db import database
from src.main import app


@pytest.fixture(autouse=True)
async def setup_database():
    """
    Fixture to set up the database connection for testing.
    This fixture connects to the database before each test and rolls back any transactions
    after each test to ensure a clean state.
    """
    await database.connect()
    tx = await database.transaction()
    yield
    await tx.rollback()
    await database.disconnect()


@pytest.fixture
async def client():
    """
    Fixture to provide an HTTP client for testing.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as c:
        yield c


@pytest.mark.anyio
async def register_user(client, valid_email, valid_password, role):
    """
    Helper function to register a user for testing.
    Also checks if the status code is correct and returns the user data.
    """
    r = await client.post(
        "/users/register",
        json={"email": valid_email, "password": valid_password, "role": role},
    )
    assert r.status_code == 201, r.text
    return r.json()


def auth_headers(token):
    """
    Helper function to create authorization headers for API requests.
    """
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.anyio
async def login_user(client, valid_email, s_password):
    """
    Helper function to login a user for testing.
    Also checks if the status code is correct and returns the access token.
    """
    r = await client.post(
        "/users/token", data={"username": valid_email, "password": s_password}
    )
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


@pytest.fixture
async def check_role_access(client, valid_password):
    """
    Fixture to check role access for different endpoints.
    This fixture takes a role and checks if the role has access to the specified endpoint.
    """

    async def _check_role_access(
        role: UserRole,
        allowed_roles: list[UserRole],
        endpoint: str,
        method: str = "GET",
        payload: dict = None,
    ):
        import uuid

        email = f"{role.value}.{uuid.uuid4().hex[:8]}@example.com"
        await register_user(client, email, valid_password, role.value)
        token = await login_user(client, email, valid_password)
        auth_header = auth_headers(token)

        if method == "GET":
            response = await client.get(endpoint, headers=auth_header)
        elif method == "POST":
            response = await client.post(endpoint, json=payload, headers=auth_header)
        elif method == "PUT":
            response = await client.put(endpoint, json=payload, headers=auth_header)
        elif method == "DELETE":
            response = await client.delete(endpoint, headers=auth_header)

        if role in allowed_roles:
            assert response.status_code != 403, f"Role {role} should have access"
        else:
            assert response.status_code == 403, f"Role {role} should not have access"

    return _check_role_access


@pytest.mark.anyio
@pytest.mark.parametrize("role", list(UserRole))
async def test_access_to_get_user_by_email(check_role_access, role):
    """
    Test access to get user by email.
    This test checks if the role has access to the endpoint /users/email/{email}.
    """
    await check_role_access(
        role=role,
        allowed_roles=[UserRole.ADMIN, UserRole.MANAGER],
        endpoint="/users/email/test@example.com",
        method="GET",
    )


@pytest.mark.anyio
@pytest.mark.parametrize("role", list(UserRole))
async def test_access_to_delete_user(check_role_access, role):
    """
    Test access to delete user.
    This test checks if the role has access to the endpoint /users/delete/{email}.
    """
    await check_role_access(
        role=role,
        allowed_roles=[UserRole.ADMIN],
        endpoint="/users/delete/test@example.com",
        method="DELETE",
    )


@pytest.mark.anyio
@pytest.mark.parametrize("role", list(UserRole))
async def test_access_to_update_user(check_role_access, role):
    """
    Test access to update user.
    This test checks if the role has access to the endpoint /users/update/{email}.
    """
    await check_role_access(
        role=role,
        allowed_roles=[UserRole.ADMIN],
        endpoint="/users/update/test@example.com",
        method="PUT",
        payload={
            "email": "new@example.com",
            "password": "NewPass1!",
            "role": "manager",
        },
    )


@pytest.mark.anyio
@pytest.mark.parametrize("role", list(UserRole))
async def test_access_to_get_all_users(check_role_access, role):
    """
    Test access to get all users.
    This test checks if the role has access to the endpoint /users/all.
    """
    await check_role_access(
        role=role,
        allowed_roles=[UserRole.ADMIN],
        endpoint="/users/all",
        method="GET",
    )


@pytest.mark.parametrize("role", list(UserRole))
@pytest.mark.anyio
async def test_access_to_get_users_by_role(check_role_access, role):
    """
    Test access to get users by role.
    This test checks if the role has access to the endpoint /users/role/{role}.
    """
    await check_role_access(
        role=role,
        allowed_roles=[UserRole.ADMIN, UserRole.MANAGER],
        endpoint="/users/role/sender",
        method="GET",
    )


@pytest.mark.anyio
async def test_token_expiry(client, valid_email, valid_password):
    """
    Test token expiration by simulating time passage.
    This test checks if the token expires after a certain period.
    Also check if the response status code is correct.
    """
    await register_user(client, valid_email, valid_password, UserRole.ADMIN)
    token = await login_user(client, valid_email, valid_password)
    auth_header = auth_headers(token)
    response = await client.get("/users/all", headers=auth_header)
    assert response.status_code == 200
    with freeze_time(
        datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES + 1)
    ):
        response = await client.get("/users/all", headers=auth_header)
        assert response.status_code == 401, "Token should be expired"
        assert "Could not validate credentials" in response.json()["detail"]
