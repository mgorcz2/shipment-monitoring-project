from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from shipment_monitoring.container import Container
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext

from shipment_monitoring.core.domain.user import UserIn, User
from shipment_monitoring.infrastructure.services.iuser import IUserService

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post("/register", response_model=User, status_code=201)
@inject
async def register_user(
        new_user: UserIn,
        service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    new_user = await service.add_user(new_user)
    return new_user.model_dump() if new_user else {}
