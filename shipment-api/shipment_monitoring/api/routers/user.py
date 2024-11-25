from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from shipment_monitoring.api.security import auth
from shipment_monitoring.container import Container
from shipment_monitoring.api.security.token import Token

from shipment_monitoring.core.domain.user import UserIn, User
from shipment_monitoring.infrastructure.dto.user import UserDTO
from shipment_monitoring.infrastructure.services.iuser import IUserService
from datetime import datetime, timedelta
router = APIRouter(
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

@router.get("/get/{username}/", response_model=UserDTO, status_code=200)
@inject
async def get_user_by_username(
    username: str,
    current_user: User = Depends(auth.get_current_user),
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict | None:
    if user := await service.get_user_by_username(username):
        return user.model_dump()
    raise HTTPException(status_code=404, detail="User not found")
        
    
@router.post("/token", response_model=Token)
@inject
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: IUserService = Depends(Provide[Container.user_service])
):
    user = await service.get_user_by_username(username=form_data.username)
    if not user or not auth.verify_password(
        form_data.password, user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}  