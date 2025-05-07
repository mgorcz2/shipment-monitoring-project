import pytest
from httpx import ASGITransport, AsyncClient

from shipment_monitoring.core.domain.user import UserRole
from shipment_monitoring.db import database
from shipment_monitoring.main import app


@pytest.fixture(autouse=True)
def s_email():
    return "sender@example.com"


@pytest.fixture(autouse=True)
def a_email():
    return "admin@example.com"


@pytest.fixture(autouse=True)
def s_pwd():
    return "SendPass1!"


@pytest.fixture(autouse=True)
def a_pwd():
    return "AdminPass1!"


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


async def register_user(client, s_email, s_pwd, role):
    r = await client.post(
        "/users/register",
        json={"email": s_email, "password": s_pwd, "role": role},
    )
    assert r.status_code == 201, r.text
    return r.json()


async def login_user(client, s_email, s_password):
    r = await client.post(
        "/users/login", data={"username": s_email, "password": s_password}
    )
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.anyio
async def test_register_user_success(client, s_email, s_pwd):
    data = await register_user(client, s_email, s_pwd, "sender")
    assert data["email"] == s_email
    assert data["role"] == "sender"
    assert "id" in data


@pytest.mark.anyio
async def test_register_user_duplicate(client, s_email, s_pwd):
    await register_user(client, s_email, s_pwd, UserRole.SENDER)
    r = await client.post(
        "/users/register",
        json={"email": s_email, "password": s_pwd, "role": UserRole.SENDER},
    )
    assert r.status_code == 400
    assert "already registered" in r.json()["detail"]


@pytest.mark.anyio
async def test_register_user_invalid_payload(client):
    r = await client.post(
        "/users/register",
        json={"email": "bad", "password": "short", "role": "no"},
    )
    assert r.status_code == 422
    assert isinstance(r.json()["detail"], list)


@pytest.mark.anyio
async def test_login_success(client, s_email, s_pwd):
    await register_user(client, s_email, s_pwd, UserRole.SENDER)
    token = await login_user(client, s_email, s_pwd)
    assert isinstance(token, str)


@pytest.mark.anyio
async def test_login_failure(client, s_email, s_pwd):
    await register_user(client, s_email, s_pwd, UserRole.SENDER)
    r = await client.post(
        "/users/login", data={"username": s_email, "password": "wrong"}
    )
    assert r.status_code == 401
    assert "Incorrect" in r.json()["detail"]


@pytest.mark.anyio
async def test_protected_endpoint_forbidden_to_non_admin(client, s_email, s_pwd):
    await register_user(client, s_email, s_pwd, UserRole.SENDER)
    token = await login_user(client, s_email, s_pwd)
    r = await client.get(f"/users/get/{s_email}", headers=auth_headers(token))
    assert r.status_code == 403


@pytest.mark.anyio
async def test_admin_can_get_all_users(client, s_email, s_pwd, a_email, a_pwd):
    await register_user(client, s_email, s_pwd, UserRole.SENDER.value)
    await register_user(client, a_email, a_pwd, UserRole.ADMIN.value)
    tok_a = await login_user(client, a_email, a_pwd)
    r = await client.get("/users/all", headers=auth_headers(tok_a))
    assert r.status_code == 200
    assert any(u["email"] == s_email for u in r.json())


@pytest.mark.anyio
async def test_sender_cannot_get_users(client, s_email, s_pwd, a_email, a_pwd):
    await register_user(client, s_email, s_pwd, UserRole.SENDER.value)
    await register_user(client, a_email, a_pwd, UserRole.ADMIN.value)

    tok_s = await login_user(client, s_email, s_pwd)
    r = await client.get("/users/all", headers=auth_headers(tok_s))
    assert r.status_code == 403


@pytest.mark.anyio
async def test_admin_can_update_user_email(client, s_email, s_pwd, a_email, a_pwd):
    await register_user(client, s_email, s_pwd, UserRole.SENDER.value)
    await register_user(client, a_email, a_pwd, UserRole.ADMIN.value)

    tok_a = await login_user(client, a_email, a_pwd)
    new_email = "new@ex.com"
    r = await client.put(
        f"/users/update/{s_email}",
        json={"email": new_email},
        headers=auth_headers(tok_a),
    )
    assert r.status_code == 200
    assert r.json()["email"] == new_email


@pytest.mark.anyio
async def test_admin_can_delete_user(client, s_email, s_pwd, a_email, a_pwd):
    await register_user(client, s_email, s_pwd, UserRole.SENDER.value)
    await register_user(client, a_email, a_pwd, UserRole.ADMIN.value)

    tok_a = await login_user(client, a_email, a_pwd)
    r = await client.delete(f"/users/delete/{s_email}", headers=auth_headers(tok_a))
    assert r.status_code == 200


@pytest.mark.anyio
async def test_get_deleted_user_returns_not_found(
    client, s_email, s_pwd, a_email, a_pwd
):
    await register_user(client, s_email, s_pwd, UserRole.SENDER.value)
    await register_user(client, a_email, a_pwd, UserRole.ADMIN.value)

    tok_a = await login_user(client, a_email, a_pwd)
    await client.delete(f"/users/delete/{s_email}", headers=auth_headers(tok_a))
    r = await client.get(f"/users/get/{s_email}", headers=auth_headers(tok_a))
    assert r.status_code == 404


@pytest.mark.anyio
@pytest.mark.parametrize("role", [UserRole.SENDER, UserRole.COURIER])
async def test_admin_can_get_users_by_role(
    client, role, a_email, a_pwd, s_email, s_pwd
):
    await register_user(client, a_email, a_pwd, UserRole.ADMIN.value)
    await register_user(client, f"{role.value}@example.com", a_pwd, role.value)
    tok_a = await login_user(client, a_email, a_pwd)

    r = await client.get(f"/users/role/{role.value}", headers=auth_headers(tok_a))
    assert r.status_code == 200
    arr = r.json()
    assert len(arr) == 1
    assert arr[0]["role"] == role.value
