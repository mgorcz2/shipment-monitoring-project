"""End to end integration tests for user in the shipment monitoring system."""

# pylint: disable=redefined-outer-name
import pytest
from httpx import ASGITransport, AsyncClient
from src.core.domain.user import UserRole
from src.db import database
from src.main import app


@pytest.fixture()
def admin_email():
    """
    Fixture to provide an admin email for testing.
    """
    return "admin@example.com"


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


def auth_headers(token):
    """
    Helper function to create authorization headers for API requests.
    """
    return {"Authorization": f"Bearer {token}"}


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


@pytest.mark.anyio
async def test_register_user_success(client, valid_email, valid_password):
    """
    Test successful user registration.
    """
    data = await register_user(client, valid_email, valid_password, "sender")
    assert data["email"] == valid_email
    assert data["role"] == "sender"
    assert "id" in data


@pytest.mark.anyio
async def test_register_user_duplicate(client, valid_email, valid_password):
    """
    Test user registration with an already registered email.
    Also check status code and error message.
    """
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
    """
    Test user registration with invalid payload.
    Also check status code and error messages.
    """
    r = await client.post(
        "/users/register",
        json={"email": "bad", "password": "short", "role": "no"},
    )
    assert r.status_code == 422
    assert "value is not a valid email address" in r.json()["detail"][0]["msg"]
    assert "should have at least 8 characters" in r.json()["detail"][1]["msg"]
    assert "Input should be" in r.json()["detail"][2]["msg"]


@pytest.mark.anyio
async def test_login_success(client, valid_email, valid_password):
    """
    Test successful user login.
    Also check status code and access token.
    """
    await register_user(client, valid_email, valid_password, UserRole.SENDER)
    token = await login_user(client, valid_email, valid_password)
    assert isinstance(token, str)


@pytest.mark.anyio
async def test_login_failure(client, valid_email, valid_password):
    """
    Test user login with incorrect password.
    Also check status code and error message.
    """
    await register_user(client, valid_email, valid_password, UserRole.SENDER)
    r = await client.post(
        "/users/token", data={"username": valid_email, "password": "wrong"}
    )
    assert r.status_code == 401
    assert "Incorrect" in r.json()["detail"]


@pytest.mark.anyio
async def test_get_user_by_email(client, admin_email, valid_password):
    """
    Test getting user by email.
    Also check status code and user data.
    """
    await register_user(client, admin_email, valid_password, UserRole.ADMIN)
    token = await login_user(client, admin_email, valid_password)
    r = await client.get(f"/users/email/{admin_email}", headers=auth_headers(token))
    assert r.status_code == 200
    assert r.json()["email"] == admin_email


@pytest.mark.anyio
async def test_get_user_by_email_not_found(
    client, admin_email, valid_email, valid_password
):
    """
    Test getting user by email that does not exist.
    Also check status code and error message.
    """
    await register_user(client, admin_email, valid_password, UserRole.ADMIN)
    token = await login_user(client, admin_email, valid_password)
    r = await client.get(f"/users/email/{valid_email}", headers=auth_headers(token))
    r = await client.get(f"/users/email/{valid_email}", headers=auth_headers(token))
    assert r.status_code == 404


@pytest.mark.anyio
async def test_get_all_users(client, valid_email, valid_password, admin_email):
    """
    Test getting all users.
    Also check status code and user data.
    """
    await register_user(client, valid_email, valid_password, UserRole.SENDER)
    await register_user(client, admin_email, valid_password, UserRole.ADMIN)
    tok_a = await login_user(client, admin_email, valid_password)
    r = await client.get("/users/all", headers=auth_headers(tok_a))
    assert r.status_code == 200
    assert any(u["email"] == valid_email for u in r.json())


@pytest.mark.anyio
async def test_update_user_email(client, valid_email, valid_password, admin_email):
    """
    Test updating user email.
    Also check status code and updated email.
    """
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
    """
    Test updating user role.
    Also check status code and updated role.
    """
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
async def test_update_user_not_found(client, valid_email, valid_password, admin_email):
    """
    Test updating user role for a user that does not exist.
    Also check status code and error message.
    """
    await register_user(client, admin_email, valid_password, UserRole.ADMIN)
    tok_a = await login_user(client, admin_email, valid_password)
    new_role = UserRole.SENDER
    r = await client.put(
        f"/users/update/{valid_email}",
        json={"role": new_role},
        headers=auth_headers(tok_a),
    )
    assert r.status_code == 404
    assert "No user found" in r.json()["detail"]


@pytest.mark.anyio
async def test_delete_user(client, valid_email, valid_password, admin_email):
    """
    Test deleting a user.
    Also check status code and user data.
    """
    await register_user(client, valid_email, valid_password, UserRole.SENDER)
    await register_user(client, admin_email, valid_password, UserRole.ADMIN)

    tok_a = await login_user(client, admin_email, valid_password)
    r = await client.delete(f"/users/delete/{valid_email}", headers=auth_headers(tok_a))
    assert r.status_code == 200


@pytest.mark.anyio
async def test_get_deleted_user_returns_not_found(
    client, valid_email, valid_password, admin_email
):
    """
    Test getting a deleted user.
    Also check status code and error message.
    """
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
    """
    Test getting users by role.
    Also check status code and user data.
    """
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
    """
    Test getting users by role that does not exist.
    Also check status code and error message.
    """
    await register_user(client, admin_email, valid_password, UserRole.ADMIN)
    tok_a = await login_user(client, admin_email, valid_password)

    r = await client.get(
        f"/users/role/{UserRole.SENDER.value}", headers=auth_headers(tok_a)
    )
    assert r.status_code == 404
    assert "No users found" in r.json()["detail"]
