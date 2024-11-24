from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException


from shipment_monitoring.container import Container


from shipment_monitoring.core.domain.user import UserIn, User
from shipment_monitoring.infrastructure.dto.user import UserDTO
from shipment_monitoring.infrastructure.services.iuser import IUserService

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post("/register/", response_model=User, status_code=201)
@inject
async def register_user(
        new_user: UserIn,
        service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    if new_user := await service.register_user(new_user):
        return new_user.model_dump()
    raise HTTPException(status_code=400, detail="Login already registered")
    

@router.get("/login/{login}/{password}", status_code=200)
@inject
async def login_user(
        login: str,
        password: str,
        service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    user = await service.login_user(login, password)
    return {"message":"ISTNIEJE TAKI"} if user else {}

@router.get("/get/{login}/", response_model=UserDTO, status_code=200)
@inject
async def get_user_by_login(
    login: str,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict | None:
    user = await service.get_user_by_login(login)
    if user := await service.get_user_by_login(login):
        return user.model_dump()
    raise HTTPException(status_code=404, detail="User not found")
        
    
    