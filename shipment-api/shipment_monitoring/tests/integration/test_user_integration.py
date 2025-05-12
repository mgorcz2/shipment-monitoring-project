import pytest
from httpx import ASGITransport, AsyncClient

from shipment_monitoring.core.domain.user import UserRole
from shipment_monitoring.db import database
from shipment_monitoring.main import app


@pytest.fixture()
def admin_email():
    return "admin@example.com"


@pytest.fixture(autouse=True)
async def setup_database():
    await database.connect()
    tx = await database.transaction()
    yield
    await tx.rollback()
    await database.disconnect()


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


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


@pytest.mark.anyio
async def login_user(client, valid_email, s_password):
    r = await client.post(
        "/users/token", data={"username": valid_email, "password": s_password}
    )
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


@pytest.mark.anyio
async def test_register_user_success(client, valid_email, valid_password):
    data = await register_user(client, valid_email, valid_password, "sender")
    assert data["email"] == valid_email
    assert data["role"] == "sender"
    assert "id" in data


@pytest.mark.anyio
async def test_register_user_duplicate(client, valid_email, valid_password):
    await register_user(client, valid_email, valid_password, UserRole.SENDER)
    r = await client.post(
        "/users/register",
        json={
            "email": valid_email,
            "password": valid_password,
            "role": UserRole.SENDER,
        },
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
async def test_login_success(client, valid_email, valid_password):
    await register_user(client, valid_email, valid_password, UserRole.SENDER)
    token = await login_user(client, valid_email, valid_password)
    assert isinstance(token, str)


@pytest.mark.anyio
async def test_login_failure(client, valid_email, valid_password):
    await register_user(client, valid_email, valid_password, UserRole.SENDER)
    r = await client.post(
        "/users/token", data={"username": valid_email, "password": "wrong"}
    )
    assert r.status_code == 401
    assert "Incorrect" in r.json()["detail"]


@pytest.mark.anyio
async def test_get_user_by_email(client, admin_email, valid_password):
    await register_user(client, admin_email, valid_password, UserRole.ADMIN)
    token = await login_user(client, admin_email, valid_password)
    r = await client.get(f"/users/email/{admin_email}", headers=auth_headers(token))
    assert r.status_code == 200
    assert r.json()["email"] == admin_email


@pytest.mark.anyio
async def test_get_user_by_email_not_found(
    client, admin_email, valid_email, valid_password
):
    await register_user(client, admin_email, valid_password, UserRole.ADMIN)
    token = await login_user(client, admin_email, valid_password)
    r = await client.get(f"/users/email/{valid_email}", headers=auth_headers(token))
    r = await client.get(f"/users/email/{valid_email}", headers=auth_headers(token))
    assert r.status_code == 404


@pytest.mark.anyio
async def test_get_all_users(client, valid_email, valid_password, admin_email):
    await register_user(client, valid_email, valid_password, UserRole.SENDER)
    await register_user(client, admin_email, valid_password, UserRole.ADMIN)
    tok_a = await login_user(client, admin_email, valid_password)
    r = await client.get("/users/all", headers=auth_headers(tok_a))
    assert r.status_code == 200
    assert any(u["email"] == valid_email for u in r.json())


@pytest.mark.anyio
async def test_update_user_email(client, valid_email, valid_password, admin_email):
    await register_user(client, valid_email, valid_password, UserRole.SENDER)
    await register_user(client, admin_email, valid_password, UserRole.ADMIN)

    tok_a = await login_user(client, admin_email, valid_password)
    new_email = "new@ex.com"
    r = await client.put(
        f"/users/update/{valid_email}",
        json={"email": new_email},
        headers=auth_headers(tok_a),
    )
    assert r.status_code == 200
    assert r.json()["email"] == new_email


@pytest.mark.anyio
@pytest.mark.parametrize(
    "role",
    list(UserRole),
)
async def test_update_user_role(client, valid_email, valid_password, admin_email, role):
    await register_user(client, valid_email, valid_password, UserRole.SENDER)
    await register_user(client, admin_email, valid_password, UserRole.ADMIN)

    tok_a = await login_user(client, admin_email, valid_password)
    new_role = role
    r = await client.put(
        f"/users/update/{valid_email}",
        json={"role": new_role},
        headers=auth_headers(tok_a),
    )
    assert r.status_code == 200
    assert r.json()["role"] == new_role


@pytest.mark.anyio
async def test_delete_user(client, valid_email, valid_password, admin_email):
    await register_user(client, valid_email, valid_password, UserRole.SENDER)
    await register_user(client, admin_email, valid_password, UserRole.ADMIN)

    tok_a = await login_user(client, admin_email, valid_password)
    r = await client.delete(f"/users/delete/{valid_email}", headers=auth_headers(tok_a))
    assert r.status_code == 200


@pytest.mark.anyio
async def test_get_deleted_user_returns_not_found(
    client, valid_email, valid_password, admin_email
):
    await register_user(client, valid_email, valid_password, UserRole.SENDER)
    await register_user(client, admin_email, valid_password, UserRole.ADMIN)

    tok_a = await login_user(client, admin_email, valid_password)
    r = await client.delete(f"/users/delete/{valid_email}", headers=auth_headers(tok_a))
    assert r.status_code == 200
    r = await client.get(f"/users/email/{valid_email}", headers=auth_headers(tok_a))
    assert r.status_code == 404


@pytest.mark.anyio
@pytest.mark.parametrize(
    "role", [UserRole.SENDER.value, UserRole.COURIER.value, UserRole.MANAGER.value]
)
async def test_get_users_by_role(client, role, admin_email, valid_password):
    await register_user(client, admin_email, valid_password, UserRole.ADMIN)
    await register_user(client, f"{role}@example.com", valid_password, role)
    tok_a = await login_user(client, admin_email, valid_password)

    r = await client.get(f"/users/role/{role}", headers=auth_headers(tok_a))
    assert r.status_code == 200
    arr = r.json()
    assert len(arr) == 1
    assert arr[0]["role"] == role


@pytest.mark.anyio
async def test_get_users_by_role_not_found(client, admin_email, valid_password):
    await register_user(client, admin_email, valid_password, UserRole.ADMIN)
    tok_a = await login_user(client, admin_email, valid_password)

    r = await client.get(
        f"/users/role/{UserRole.SENDER.value}", headers=auth_headers(tok_a)
    )
    assert r.status_code == 404
    assert "No users found" in r.json()["detail"]
