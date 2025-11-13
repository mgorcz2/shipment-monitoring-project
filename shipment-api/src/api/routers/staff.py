from typing import Iterable
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from src.container import Container
from src.core.domain.user import StaffIn, User, UserIn, UserRole
from src.core.security import auth
from src.infrastructure.dto.userDTO import StaffDTO
from src.infrastructure.services.istaff import IStaffService

router = APIRouter(
    prefix="/staff",
    tags=["staff"],
)


@auth.role_required([UserRole.ADMIN])
@router.post("/register", response_model=StaffDTO, status_code=status.HTTP_201_CREATED)
@inject
async def register_staff_with_user(
    staff: StaffIn,
    user_data: UserIn,
    current_user: User = Depends(auth.get_current_user),
    service: IStaffService = Depends(Provide[Container.staff_service]),
) -> StaffDTO:
    try:
        return await service.register_staff_with_user(staff, user_data)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@auth.role_required([UserRole.ADMIN])
@router.get("/{user_id}", response_model=StaffDTO)
@inject
async def get_staff(
    user_id: UUID,
    current_user: User = Depends(auth.get_current_user),
    service: IStaffService = Depends(Provide[Container.staff_service]),
) -> StaffDTO:
    try:
        return await service.get_staff(user_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@auth.role_required([UserRole.ADMIN])
@router.put("/{user_id}", response_model=StaffDTO)
@inject
async def update_staff(
    user_id: UUID,
    data: StaffIn,
    current_user: User = Depends(auth.get_current_user),
    service: IStaffService = Depends(Provide[Container.staff_service]),
) -> StaffDTO:
    try:
        return await service.update_staff(user_id, data)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@auth.role_required([UserRole.ADMIN])
@router.delete("/{user_id}", response_model=StaffDTO)
@inject
async def delete_staff(
    user_id: UUID,
    current_user: User = Depends(auth.get_current_user),
    service: IStaffService = Depends(Provide[Container.staff_service]),
) -> StaffDTO:
    try:
        return await service.delete_staff(user_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@auth.role_required([UserRole.ADMIN])
@router.get("/", response_model=Iterable[StaffDTO])
@inject
async def get_all_staff(
    current_user: User = Depends(auth.get_current_user),
    service: IStaffService = Depends(Provide[Container.staff_service]),
) -> Iterable[StaffDTO]:
    return await service.get_all_staff()
