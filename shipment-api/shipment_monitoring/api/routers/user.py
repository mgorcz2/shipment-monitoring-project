from typing import Iterable

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from shipment_monitoring.container import Container
from shipment_monitoring.core.domain.user import User, UserIn, UserRole, UserUpdate
from shipment_monitoring.core.security import auth
from shipment_monitoring.infrastructure.dto.tokenDTO import TokenDTO
from shipment_monitoring.infrastructure.dto.userDTO import UserDTO
from shipment_monitoring.infrastructure.services.iuser import IUserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/register", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
@inject
async def register_user(
    new_user: UserIn,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> UserDTO:
    """An endpoint for registering new user.

    Args:
        new_user (UserIn): The user input data.
        service (IUserService): The injected user service.

    Returns:
        UserDTO: The user DTO details.
    """
    try:
        user = await service.register_user(new_user)
        return user
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.post("/token", response_model=TokenDTO)
@inject
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: IUserService = Depends(Provide[Container.user_service]),
) -> TokenDTO:
    """An endpoint for authenticating users(creating token)

    Args:
        form_data (OAuth2PasswordRequestForm, optional): The user input data from request form.
        service (IUserService): The injected user service.

    Returns:
        TokenDTO: The token DTO details.
    """
    try:
        token = await service.login_for_access_token(
            form_data.username, form_data.password
        )
        return token
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))


@router.get("/email/{email}", response_model=UserDTO, status_code=status.HTTP_200_OK)
@auth.role_required([UserRole.ADMIN, UserRole.MANAGER])
@inject
async def get_user_by_email(
    email: str,
    current_user: User = Depends(auth.get_current_user),
    service: IUserService = Depends(Provide[Container.user_service]),
) -> UserDTO:
    """The endpoint getting user by provided email.

    Args:
        email (str): The email of the user.
        current_user (User): The currently injected authenticated user.
        service (IUserService): The injected user service.

    Returns:
        UserDTO: The user DTO details if exists.
    """
    try:
        user = await service.get_user_by_email(email)
        return user
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


@router.delete("/delete/{email}", status_code=status.HTTP_200_OK)
@auth.role_required(UserRole.ADMIN)
@inject
async def delete_user(
    email: str,
    current_user: User = Depends(auth.get_current_user),
    service: IUserService = Depends(Provide[Container.user_service]),
) -> User:
    """The endpoint deleting user by provided email.

    Args:
        email (str): The email of the user.
        current_user (User): The currently injected authenticated user.
        service (IUserService): The injected user service.

    Returns:
        dict: The deleted user object.
    """
    try:
        user = await service.detele_user(email)
        return user
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


@router.put("/update/{email}", status_code=status.HTTP_200_OK)
@auth.role_required(UserRole.ADMIN)
@inject
async def update_user(
    email: str,
    data: UserUpdate,
    current_user: User = Depends(auth.get_current_user),
    service: IUserService = Depends(Provide[Container.user_service]),
) -> User:
    """The endpoint updating user by provided email.

    Args:
        email (str): The email of the user.
        data (User): The updated user details.
        current_user (User): The currently injected authenticated user.
        service (IUserService): The injected user service.

    Returns:
        dict: The updated user object if updated.
    """
    try:
        user = await service.update_user(email, data)
        return user
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.get("/all", status_code=status.HTTP_200_OK)
@auth.role_required(UserRole.ADMIN)
@inject
async def get_all_users(
    current_user: User = Depends(auth.get_current_user),
    service: IUserService = Depends(Provide[Container.user_service]),
) -> Iterable[UserDTO]:
    """The endpoint getting all users.

    Args:
    current_user (User): The currently injected authenticated user.
    service (IUserService): The injected user service.

    Returns:
         Iterable[UserDTO]: The user objects DTO details.
    """
    try:
        users = await service.get_all_users()
        return users
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.get("/role/{role}", status_code=status.HTTP_200_OK)
@auth.role_required([UserRole.ADMIN, UserRole.MANAGER])
@inject
async def get_users_by_role(
    role: UserRole,
    current_user: User = Depends(auth.get_current_user),
    service: IUserService = Depends(Provide[Container.user_service]),
) -> Iterable[UserDTO]:
    """The endpoint getting users by role.

    Args:
        role (UserRole): The role of the users.
        current_user (User): The currently injected authenticated user.
        service (IUserService): The injected user service.

    Returns:
        Iterable[UserDTO]: The user objects DTO details.
    """
    try:
        users = await service.get_users_by_role(role)
        return users
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
