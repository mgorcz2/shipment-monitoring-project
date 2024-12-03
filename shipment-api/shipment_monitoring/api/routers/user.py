from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from shipment_monitoring.container import Container
from shipment_monitoring.infrastructure.dto.tokenDTO import TokenDTO
from shipment_monitoring.core.domain.user import UserIn, User
from shipment_monitoring.infrastructure.dto.userDTO import UserDTO
from shipment_monitoring.infrastructure.services.iuser import IUserService



router = APIRouter(
    tags=["user"],
)

@router.post("/register/", response_model=UserDTO, status_code=201)
@inject
async def register_user(
        new_user: UserIn,
        service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    try:    #lapanie bledow
        user = await service.register_user(new_user)
        return user.model_dump()
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    
@router.get("/get/{username}/", response_model=User, status_code=200)
@inject
async def get_user_by_username(
    username: str,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict | None:
    if user := await service.get_user_by_username(username):
        return user
    raise HTTPException(status_code=404, detail="User not found")
        
    
@router.post("/token", response_model=TokenDTO)
@inject
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: IUserService = Depends(Provide[Container.user_service])
):
    try:
        token = await service.login_for_access_token(form_data.username, form_data.password)
        return token
    except ValueError as error:
        raise HTTPException(status_code=401, detail=str(error))