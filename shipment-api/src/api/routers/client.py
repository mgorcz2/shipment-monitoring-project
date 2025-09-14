from typing import Iterable
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from src.container import Container
from src.core.domain.user import ClientIn
from src.infrastructure.dto.userDTO import ClientDTO
from src.infrastructure.services.iclient import IClientService

router = APIRouter(
    prefix="/client",
    tags=["client"],
)


@router.post("/register", response_model=ClientDTO, status_code=status.HTTP_201_CREATED)
@inject
async def register_client(
    client: ClientIn,
    user_id: UUID,
    service: IClientService = Depends(Provide[Container.client_service]),
) -> ClientDTO:
    try:
        return await service.register_client(client, user_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/{user_id}", response_model=ClientDTO)
@inject
async def get_client(
    user_id: UUID,
    service: IClientService = Depends(Provide[Container.client_service]),
) -> ClientDTO:
    try:
        return await service.get_client(user_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.put("/{user_id}", response_model=ClientDTO)
@inject
async def update_client(
    user_id: UUID,
    data: ClientIn,
    service: IClientService = Depends(Provide[Container.client_service]),
) -> ClientDTO:
    try:
        return await service.update_client(user_id, data)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.delete("/{user_id}", response_model=ClientDTO)
@inject
async def delete_client(
    user_id: UUID,
    service: IClientService = Depends(Provide[Container.client_service]),
) -> ClientDTO:
    try:
        return await service.delete_client(user_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get("/", response_model=Iterable[ClientDTO])
@inject
async def get_all_clients(
    service: IClientService = Depends(Provide[Container.client_service]),
) -> Iterable[ClientDTO]:
    return await service.get_all_clients()
