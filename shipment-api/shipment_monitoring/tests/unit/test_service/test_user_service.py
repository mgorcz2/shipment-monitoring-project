from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
from jose import jwt

import shipment_monitoring.infrastructure.services.user as user_service_module
from shipment_monitoring.config import config
from shipment_monitoring.core.domain.user import UserIn, UserRole, UserUpdate
from shipment_monitoring.core.security import consts
from shipment_monitoring.core.security.token import create_access_token
from shipment_monitoring.infrastructure.dto.userDTO import UserDTO
from shipment_monitoring.infrastructure.services.user import UserService


@pytest.fixture
def repo_mock(mocker):
    return mocker.AsyncMock()


@pytest.fixture(autouse=True)
def patch_hash_and_token(mocker):
    mocker.patch.object(
        user_service_module.password_hashing,
        "hash_password",
        lambda pwd: f"hashed-{pwd}",
    )
    mocker.patch.object(
        user_service_module.password_hashing,
        "verify_password",
        lambda pwd, hashed: hashed == f"hashed-{pwd}",
    )
    mocker.patch.object(
        user_service_module,
        "create_access_token",
        lambda data: "service-token",
    )


@pytest.fixture
def user_service(repo_mock):
    return UserService(repo_mock)


@pytest.fixture
def sample_record():
    raw = "Password123"
    return {
        "id": uuid4(),
        "email": "user@example.com",
        "password": f"hashed-{raw}",
        "role": "sender",
    }


@pytest.fixture
def sample_user_in(sample_record):
    return UserIn(
        email=sample_record["email"],
        password=sample_record["password"],
        role=UserRole.SENDER,
    )


@pytest.mark.anyio
async def test_register_user_success(
    user_service, repo_mock, sample_record, sample_user_in
):
    repo_mock.get_user_by_email.return_value = None
    repo_mock.register_user.return_value = sample_record
    dto = await user_service.register_user(sample_user_in)

    repo_mock.get_user_by_email.assert_awaited_once_with(sample_record["email"])
    repo_mock.register_user.assert_awaited_once()
    assert isinstance(dto, UserDTO)
    assert dto.email == sample_record["email"]


@pytest.mark.anyio
async def test_register_user_duplicate(
    user_service, repo_mock, sample_record, sample_user_in
):
    repo_mock.get_user_by_email.return_value = sample_record
    with pytest.raises(ValueError, match="User with that email already registered."):
        await user_service.register_user(sample_user_in)


@pytest.mark.anyio
async def test_register_user_failed(user_service, repo_mock, sample_user_in):
    repo_mock.get_user_by_email.return_value = None
    repo_mock.register_user.return_value = None
    with pytest.raises(
        ValueError, match="Failed to register the user. Please try again."
    ):
        await user_service.register_user(sample_user_in)


@pytest.mark.anyio
async def test_get_user_by_id_found(user_service, repo_mock, sample_record):
    repo_mock.get_user_by_id.return_value = sample_record
    dto = await user_service.get_user_by_id(sample_record["id"])
    repo_mock.get_user_by_id.assert_awaited_once_with(sample_record["id"])
    assert isinstance(dto, UserDTO)
    assert dto.id == sample_record["id"]


@pytest.mark.anyio
async def test_get_user_by_id_not_found(user_service, repo_mock):
    repo_mock.get_user_by_id.return_value = None
    with pytest.raises(ValueError, match="No user found with the provided ID"):
        await user_service.get_user_by_id(uuid4())


@pytest.mark.anyio
async def test_get_user_by_email_found(user_service, repo_mock, sample_record):
    repo_mock.get_user_by_email.return_value = sample_record
    dto = await user_service.get_user_by_email(sample_record["email"])
    repo_mock.get_user_by_email.assert_awaited_once_with(sample_record["email"])
    assert isinstance(dto, UserDTO)
    assert dto.email == sample_record["email"]


@pytest.mark.anyio
async def test_get_user_by_email_not_found(user_service, repo_mock):
    repo_mock.get_user_by_email.return_value = None
    with pytest.raises(ValueError, match="No user found with the provided email"):
        await user_service.get_user_by_email("no@one.com")


@pytest.mark.anyio
async def test_delete_user_found(user_service, repo_mock, sample_record):
    repo_mock.detele_user.return_value = sample_record
    result = await user_service.detele_user(sample_record["email"])
    repo_mock.detele_user.assert_awaited_once_with(sample_record["email"])
    assert result == sample_record


@pytest.mark.anyio
async def test_delete_user_not_found(user_service, repo_mock):
    repo_mock.detele_user.return_value = None
    with pytest.raises(ValueError, match="No user found with the provided email"):
        await user_service.detele_user("no@one.com")


@pytest.mark.anyio
async def test_update_user_not_found(user_service, repo_mock):
    repo_mock.get_user_by_email.return_value = None
    update = UserUpdate(email="new@e.com")
    with pytest.raises(ValueError, match="No user found with the provided email"):
        await user_service.update_user("old@e.com", update)


@pytest.mark.anyio
async def test_update_user_email_conflict(user_service, repo_mock, sample_record):
    repo_mock.get_user_by_email.side_effect = [sample_record, sample_record]
    update = UserUpdate(email="other@e.com")
    with pytest.raises(ValueError, match="User with that email already registered"):
        await user_service.update_user(sample_record["email"], update)


@pytest.mark.anyio
async def test_update_user_failed(user_service, repo_mock, sample_record):
    repo_mock.get_user_by_email.return_value = sample_record
    repo_mock.update_user.return_value = None
    with pytest.raises(
        ValueError, match="Failed to update the user. Please try again."
    ):
        await user_service.update_user(sample_record["email"], UserUpdate())


@pytest.mark.anyio
async def test_update_user_success(user_service, repo_mock, sample_record, mocker):
    repo_mock.get_user_by_email.side_effect = [sample_record, None]
    hashed = f"hashed-{sample_record['password']}"
    updated_rec = sample_record.copy()
    updated_rec["email"] = "new@e.com"
    updated_rec["password"] = hashed
    repo_mock.update_user.return_value = updated_rec

    update = UserUpdate(
        email="new@e.com", password=sample_record["password"], role=UserRole.SENDER
    )
    result = await user_service.update_user(sample_record["email"], update)
    assert result["email"] == "new@e.com"
    assert result["password"] == hashed


@pytest.mark.anyio
async def test_get_all_users(user_service, repo_mock, sample_record):
    repo_mock.get_all_users.return_value = [sample_record]
    result = await user_service.get_all_users()
    assert isinstance(result, list)
    assert result[0].email == sample_record["email"]


@pytest.mark.anyio
async def test_get_all_users_not_found(user_service, repo_mock):
    repo_mock.get_all_users.return_value = []
    with pytest.raises(ValueError, match="No users found"):
        await user_service.get_all_users()


@pytest.mark.anyio
async def test_get_users_by_role(user_service, repo_mock, sample_record):
    repo_mock.get_users_by_role.return_value = [sample_record]
    result = await user_service.get_users_by_role(UserRole.SENDER)
    assert isinstance(result, list)
    assert sample_record["email"] in [user.email for user in result]


@pytest.mark.anyio
async def test_get_users_by_role_not_found(user_service, repo_mock):
    repo_mock.get_users_by_role.return_value = []
    with pytest.raises(ValueError, match="No users found"):
        await user_service.get_users_by_role(UserRole.SENDER)


@pytest.mark.anyio
async def test_login_for_access_token_success(
    user_service, repo_mock, sample_record, mocker
):
    user_mock = mocker.Mock()
    user_mock.email = sample_record["email"]
    user_mock.password = sample_record["password"]
    repo_mock.get_user_by_email.return_value = user_mock
    token = await user_service.login_for_access_token(
        sample_record["email"], "Password123"
    )
    repo_mock.get_user_by_email.assert_awaited_once_with(email=sample_record["email"])
    assert isinstance(token, dict)
    assert token["access_token"] == "service-token"
    assert token["token_type"] == "bearer"


@pytest.mark.anyio
async def test_login_for_access_token_user_not_found(
    user_service, repo_mock, sample_record
):
    repo_mock.get_user_by_email.return_value = None
    with pytest.raises(ValueError, match="Incorrect email or password"):
        await user_service.login_for_access_token(sample_record["email"], "Password123")


@pytest.mark.anyio
async def test_login_for_access_token_invalid_password(
    user_service, repo_mock, sample_record, mocker
):
    user_mock = mocker.Mock()
    user_mock.email = sample_record["email"]
    user_mock.password = sample_record["password"]
    repo_mock.get_user_by_email.return_value = user_mock
    with pytest.raises(ValueError, match="Incorrect email or password"):
        await user_service.login_for_access_token(
            sample_record["email"], "wrongpassword"
        )


# Token Tests
class MockDateTime:
    @classmethod
    def now(cls, tz=None):
        return datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)


@pytest.fixture()
def patch_datetime(monkeypatch):
    import shipment_monitoring.core.security.token as token_module

    monkeypatch.setattr(token_module, "datetime", MockDateTime)
    monkeypatch.setattr(config, "SECRET_KEY", "test-secret")


@pytest.mark.usefixtures("patch_datetime")
def test_create_access_token_default_expiry():
    payload = {"sub": "abc123"}
    token = create_access_token(payload)
    decoded = jwt.decode(
        token,
        config.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
        options={"verify_exp": False},
    )
    assert decoded["sub"] == "abc123"
    expected_exp = int(
        (
            MockDateTime.now() + timedelta(minutes=consts.ACCESS_TOKEN_EXPIRE_MINUTES)
        ).timestamp()
    )
    assert decoded["exp"] == expected_exp


@pytest.mark.usefixtures("patch_datetime")
def test_create_access_token_expired_error():
    payload = {"sub": "abc123"}
    token = create_access_token(payload)
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(token, config.SECRET_KEY, algorithms=[consts.ALGORITHM])


def test_create_access_token_without_sub():
    payload = {"sub": ""}
    with pytest.raises(
        ValueError, match="Token payload must contain a non-empty 'sub'"
    ):
        create_access_token(payload)


def test_create_access_token_contains_sub():
    payload = {"sub": "abc123"}
    token = create_access_token(payload)
    decoded = jwt.decode(
        token,
        config.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
        options={"verify_exp": False},
    )
    assert decoded["sub"] == "abc123"


def test_access_token_incorrect_secret():
    payload = {"sub": "abc123"}
    token = create_access_token(payload)
    with pytest.raises(jwt.JWTError):
        jwt.decode(token, "wrong-secret", algorithms=[consts.ALGORITHM])
