import pytest
from httpx import ASGITransport, AsyncClient

from shipment_monitoring.core.domain.user import UserRole
from shipment_monitoring.db import database
from shipment_monitoring.main import app


@pytest.fixture(autouse=True)
async def setup_database():
    await database.connect()
    tx = await database.transaction()
    yield
    await tx.rollback()
    await database.disconnect()


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as c:
        yield c


@pytest.mark.anyio
async def register_user(client, valid_email, valid_password, role):
    r = await client.post(
        "/users/register",
        json={"email": valid_email, "password": valid_password, "role": role},
    )
    assert r.status_code == 201, r.text
    return r.json()


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.anyio
async def login_user(client, valid_email, s_password):
    r = await client.post(
        "/users/token", data={"username": valid_email, "password": s_password}
    )
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


@pytest.fixture
async def check_role_access(client, valid_password):
    async def _check_role_access(
        role: UserRole,
        allowed_roles: list[UserRole],
        endpoint: str,
        method: str = "GET",
        payload: dict = None,
    ):
        email = f"{role.value}@example.com"
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
    await check_role_access(
        role=role,
        allowed_roles=[UserRole.ADMIN, UserRole.MANAGER],
        endpoint="/users/email/test@example.com",
        method="GET",
    )


@pytest.mark.anyio
@pytest.mark.parametrize("role", list(UserRole))
async def test_access_to_delete_user(check_role_access, role):
    await check_role_access(
        role=role,
        allowed_roles=[UserRole.ADMIN],
        endpoint="/users/delete/test@example.com",
        method="DELETE",
    )


@pytest.mark.anyio
@pytest.mark.parametrize("role", list(UserRole))
async def test_access_to_update_user(check_role_access, role):
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
    await check_role_access(
        role=role,
        allowed_roles=[UserRole.ADMIN],
        endpoint="/users/all",
        method="GET",
    )


@pytest.mark.parametrize("role", list(UserRole))
@pytest.mark.anyio
async def test_access_to_get_users_by_role(check_role_access, role):
    await check_role_access(
        role=role,
        allowed_roles=[UserRole.ADMIN, UserRole.MANAGER],
        endpoint="/users/role/sender",
        method="GET",
    )
