from typing import Iterable
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from src.container import Container
from src.core.domain.user import StaffIn
from src.infrastructure.dto.userDTO import StaffDTO
from src.infrastructure.services.istaff import IStaffService

router = APIRouter(
    prefix="/staff",
    tags=["staff"],
)


@router.post("/register", response_model=StaffDTO, status_code=status.HTTP_201_CREATED)
@inject
async def register_staff(
    staff: StaffIn,
    user_id: UUID,
    service: IStaffService = Depends(Provide[Container.staff_service]),
) -> StaffDTO:
    try:
        return await service.register_staff(staff, user_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/{user_id}", response_model=StaffDTO)
@inject
async def get_staff(
    user_id: UUID,
    service: IStaffService = Depends(Provide[Container.staff_service]),
) -> StaffDTO:
    try:
        return await service.get_staff(user_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.put("/{user_id}", response_model=StaffDTO)
@inject
async def update_staff(
    user_id: UUID,
    data: StaffIn,
    service: IStaffService = Depends(Provide[Container.staff_service]),
) -> StaffDTO:
    try:
        return await service.update_staff(user_id, data)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.delete("/{user_id}", response_model=StaffDTO)
@inject
async def delete_staff(
    user_id: UUID,
    service: IStaffService = Depends(Provide[Container.staff_service]),
) -> StaffDTO:
    try:
        return await service.delete_staff(user_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get("/", response_model=Iterable[StaffDTO])
@inject
async def get_all_staff(
    service: IStaffService = Depends(Provide[Container.staff_service]),
) -> Iterable[StaffDTO]:
    return await service.get_all_staff()
