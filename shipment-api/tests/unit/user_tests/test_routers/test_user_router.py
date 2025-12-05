"""Unit tests for User router."""

# pylint: disable=redefined-outer-name
from types import SimpleNamespace
from uuid import uuid4

import pytest
import src.api.routers.user as user_router
from fastapi import HTTPException, status
from src.core.domain.user import User, UserIn, UserRole
from src.infrastructure.dto.tokenDTO import TokenDTO
from src.infrastructure.dto.userDTO import UserDTO


@pytest.fixture
def mock_user_service(mocker):
    """
    Mock the user service for testing.
    """
    return mocker.AsyncMock()


@pytest.fixture(
    params=[UserRole.ADMIN, UserRole.CLIENT, UserRole.COURIER, UserRole.MANAGER]
)
def user(request):
    return User(
        id=uuid4(),
        email="user@example.com",
        password="Password123",
        role=request.param,
    )


@pytest.mark.anyio
async def test_register_user_success(mock_user_service, valid_userin, valid_userDTO):
    """
    Test the register_user function
    with a valid user input and check if the returned DTO matches the expected one.
    """
    in_user = valid_userin
    expected = valid_userDTO
    mock_user_service.register_user.return_value = expected
    dto = await user_router.register_user(new_user=in_user, service=mock_user_service)
    assert isinstance(dto, UserDTO)
    assert dto.email == expected.email
    mock_user_service.register_user.assert_awaited_once_with(in_user)


@pytest.mark.anyio
async def test_register_user_failure(mock_user_service):
    """
    Test the register_user function with an invalid user input
    and check if it raises an HTTPException with the correct status code and detail.
    """
    in_data = UserIn(email="x@y.z", password="Password1", role=UserRole.COURIER)
    mock_user_service.register_user.side_effect = ValueError("error")
    with pytest.raises(HTTPException) as exc:
        await user_router.register_user(new_user=in_data, service=mock_user_service)
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.detail == "error"


@pytest.mark.anyio
async def test_token_success(mock_user_service):
    """
    Test the login_for_access_token function with valid credentials
    and check if the returned DTO matches the expected one.
    """
    form = SimpleNamespace(username="u@e", password="pw")
    expected = TokenDTO(access_token="tok", token_type="bearer")
    mock_user_service.login_for_access_token.return_value = expected

    dto = await user_router.login_for_access_token(
        form_data=form,
        service=mock_user_service,
    )

    assert dto.access_token == "tok"
    assert dto.token_type == "bearer"
    mock_user_service.login_for_access_token.assert_awaited_once_with("u@e", "pw")


@pytest.mark.anyio
async def test_token_failure(mock_user_service):
    """
    Test the login_for_access_token function with invalid credentials
    and check if it raises an HTTPException with the correct status code and detail.
    """
    form = SimpleNamespace(username="u@e", password="pw")
    mock_user_service.login_for_access_token.side_effect = ValueError("nope")

    with pytest.raises(HTTPException) as exc:
        await user_router.login_for_access_token(
            form_data=form,
            service=mock_user_service,
        )

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "nope"
    mock_user_service.login_for_access_token.assert_awaited_once_with("u@e", "pw")


@pytest.mark.anyio
async def test_get_user_by_email_success(mock_user_service, user, valid_userDTO):
    """
    Test the get_user_by_email function with a valid email
    and check if the returned DTO matches the expected one.
    Also check if the function raises an HTTPException with the correct status code and detail
    """
    dto = valid_userDTO
    mock_user_service.get_user_by_email.return_value = dto
    if user.role in [UserRole.ADMIN, UserRole.MANAGER]:
        result = await user_router.get_user_by_email(
            email=valid_userDTO.email, current_user=user, service=mock_user_service
        )
        assert result.email == valid_userDTO.email
        assert result.id == valid_userDTO.id
    else:
        with pytest.raises(
            HTTPException, match="No permission to access this resource."
        ):
            await user_router.get_user_by_email(
                email=valid_userDTO.email, current_user=user, service=mock_user_service
            )


@pytest.mark.anyio
async def test_get_user_by_email_not_found(mock_user_service, user):
    """
    Test the get_user_by_email function with an invalid email
    and check if it raises an HTTPException with the correct status code and detail.
    Also check if the function raises an HTTPException with the correct status code and detail
    when the user is not an admin or manager.
    """
    mock_user_service.get_user_by_email.side_effect = ValueError("Error")
    if user.role in [UserRole.ADMIN, UserRole.MANAGER]:
        with pytest.raises(HTTPException) as exc:
            await user_router.get_user_by_email(
                email="x@y.z", current_user=user, service=mock_user_service
            )
        assert exc.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc.value.detail == "Error"
    else:
        with pytest.raises(
            HTTPException, match="No permission to access this resource."
        ):
            await user_router.get_user_by_email(
                email="x@y.z", current_user=user, service=mock_user_service
            )


@pytest.mark.anyio
async def test_delete_user_success(mock_user_service, user, valid_user):
    """
    Test the delete_user function with a valid email
    and check if the returned DTO matches the expected one.
    Also check if the function raises an HTTPException with the correct status code and detail
    when the user is not an admin.
    """
    mock_user_service.detele_user.return_value = valid_user
    if user.role == UserRole.ADMIN:
        deleted = await user_router.delete_user(
            email="u@v.w", current_user=user, service=mock_user_service
        )
        assert isinstance(deleted, User)
        assert deleted.id == valid_user.id
    else:
        with pytest.raises(
            HTTPException, match="No permission to access this resource."
        ):
            await user_router.delete_user(
                email="u@v.w", current_user=user, service=mock_user_service
            )


@pytest.mark.anyio
async def test_delete_user_not_found(mock_user_service, user):
    """
    Test the delete_user function with an invalid email
    and check if it raises an HTTPException with the correct status code and detail.
    Also check if the function raises an HTTPException with the correct status code and detail
    when the user is not an admin.
    """
    mock_user_service.detele_user.side_effect = ValueError("not found")

    if user.role == UserRole.ADMIN:
        with pytest.raises(HTTPException) as exc:
            await user_router.delete_user(
                email="absent@none", current_user=user, service=mock_user_service
            )
        assert exc.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc.value.detail == "not found"
    else:
        with pytest.raises(
            HTTPException, match="No permission to access this resource."
        ):
            await user_router.delete_user(
                email="absent@none", current_user=user, service=mock_user_service
            )


@pytest.mark.anyio
async def test_update_user_success(
    mock_user_service, user, valid_user_update, valid_user
):
    """
    Test the update_user function with a valid email
    and check if the returned DTO matches the expected one.
    Also check if the function raises an HTTPException with the correct status code and detail
    when the user is not an admin.
    """
    mock_user_service.update_user.return_value = valid_user

    if user.role == UserRole.ADMIN:
        updated = await user_router.update_user(
            email=valid_user.email,
            data=valid_user_update,
            current_user=user,
            service=mock_user_service,
        )
        assert updated.email == valid_user.email
        mock_user_service.update_user.assert_awaited_once_with(
            valid_user.email, valid_user_update
        )
    else:
        with pytest.raises(
            HTTPException, match="No permission to access this resource."
        ):
            await user_router.update_user(
                email=valid_user_update.email,
                data=valid_user_update,
                current_user=user,
                service=mock_user_service,
            )


@pytest.mark.anyio
async def test_update_user_bad_request(mock_user_service, user, valid_user_update):
    """
    Test the update_user function with an invalid email
    and check if it raises an HTTPException with the correct status code and detail.
    Also check if the function raises an HTTPException with the correct status code and detail
    when the user is not an admin.
    """
    mock_user_service.update_user.side_effect = ValueError("Error")
    if user.role == UserRole.ADMIN:
        with pytest.raises(HTTPException) as exc:
            await user_router.update_user(
                email=valid_user_update.email,
                data=valid_user_update,
                current_user=user,
                service=mock_user_service,
            )
        assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
        assert exc.value.detail == "Error"
    else:
        with pytest.raises(
            HTTPException, match="No permission to access this resource."
        ):
            await user_router.update_user(
                email=valid_user_update.email,
                data=valid_user_update,
                current_user=user,
                service=mock_user_service,
            )


@pytest.mark.anyio
async def test_get_all_users_success(mock_user_service, user):
    """
    Test the get_all_users function with a valid email
    and check if the returned DTO matches the expected one.
    Also check if the function raises an HTTPException with the correct status code and detail
    when the user is not an admin.
    """
    if user.role == UserRole.ADMIN:
        arr = [
            UserDTO(id=uuid4(), email="a@b.c", role=UserRole.ADMIN),
            UserDTO(id=uuid4(), email="d@e.f", role=UserRole.COURIER),
        ]
        mock_user_service.get_all_users.return_value = arr

        dto = await user_router.get_all_users(
            current_user=user, service=mock_user_service
        )

        assert isinstance(dto, list)
        assert len(dto) == 2
        mock_user_service.get_all_users.assert_awaited_once()
    else:
        with pytest.raises(
            HTTPException, match="No permission to access this resource."
        ):
            await user_router.get_all_users(
                current_user=user, service=mock_user_service
            )


@pytest.mark.anyio
async def test_get_all_users_not_found(mock_user_service, user):
    """
    Test the get_all_users function with an invalid email
    and check if it raises an HTTPException with the correct status code and detail.
    Also check if the function raises an HTTPException with the correct status code and detail
    when the user is not an admin.
    """
    mock_user_service.get_all_users.side_effect = ValueError("none")
    if user.role == UserRole.ADMIN:
        with pytest.raises(HTTPException) as exc:
            await user_router.get_all_users(
                current_user=user, service=mock_user_service
            )
        assert exc.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc.value.detail == "none"
    else:
        with pytest.raises(
            HTTPException, match="No permission to access this resource."
        ):
            await user_router.get_all_users(
                current_user=user, service=mock_user_service
            )


@pytest.mark.anyio
async def test_get_users_by_role_success(mock_user_service, user):
    """
    Test the get_users_by_role function with a valid email
    and check if the returned DTO matches the expected one.
    Also check if the function raises an HTTPException with the correct status code and detail
    when the user is not an admin.
    """
    if user.role in [UserRole.ADMIN, UserRole.MANAGER]:
        arr = [
            UserDTO(id=uuid4(), email="x@y.z", role=UserRole.CLIENT),
        ]
        mock_user_service.get_users_by_role.return_value = arr

        dto = await user_router.get_users_by_role(
            role=UserRole.CLIENT, current_user=user, service=mock_user_service
        )
        assert len(dto) == 1
        mock_user_service.get_users_by_role.assert_awaited_once_with(UserRole.CLIENT)
    else:
        with pytest.raises(
            HTTPException, match="No permission to access this resource."
        ):
            await user_router.get_users_by_role(
                role=UserRole.CLIENT, current_user=user, service=mock_user_service
            )


@pytest.mark.anyio
async def test_get_users_by_role_not_found(mock_user_service, user):
    """
    Test the get_users_by_role function with an invalid email
    and check if it raises an HTTPException with the correct status code and detail.
    Also check if the function raises an HTTPException with the correct status code and detail
    when the user is not an admin.
    """
    mock_user_service.get_users_by_role.side_effect = ValueError("none")
    if user.role in [UserRole.ADMIN, UserRole.MANAGER]:
        with pytest.raises(HTTPException) as exc:
            await user_router.get_users_by_role(
                role=UserRole.CLIENT, current_user=user, service=mock_user_service
            )
        assert exc.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc.value.detail == "none"
    else:
        with pytest.raises(
            HTTPException, match="No permission to access this resource."
        ):
            await user_router.get_users_by_role(
                role=UserRole.CLIENT, current_user=user, service=mock_user_service
            )
