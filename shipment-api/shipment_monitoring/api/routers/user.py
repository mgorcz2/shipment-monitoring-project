from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from shipment_monitoring.container import Container
from shipment_monitoring.infrastructure.dto.tokenDTO import TokenDTO
from shipment_monitoring.core.domain.user import UserIn, User
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
    service: IUserService = Depends(Provide[Container.user_service])
) -> TokenDTO:
    """An endpoint for authenticating users(creating token)

    Args:
        form_data (OAuth2PasswordRequestForm, optional): The user input data from request form.
        service (IUserService): The injected user service.

    Returns:
        TokenDTO: The token DTO details.
    """
    try:
        token = await service.login_for_access_token(form_data.username, form_data.password)
        return token
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))