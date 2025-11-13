"""Router for package endpoints."""

from typing import Iterable
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from src.container import Container
from src.core.domain.shipment import Package, PackageIn, ShipmentIn
from src.core.domain.user import User, UserRole
from src.core.security import auth
from src.infrastructure.dto.shipmentDTO import PackageDTO
from src.infrastructure.services.ipackage import IPackageService

router = APIRouter(
    prefix="/packages",
    tags=["packages"],
)


@router.post("/add", response_model=PackageDTO, status_code=status.HTTP_201_CREATED)
@inject
async def create_package_with_shipment(
    package: PackageIn,
    shipment_data: ShipmentIn,
    current_user: User = Depends(auth.get_current_user),
    service: IPackageService = Depends(Provide[Container.package_service]),
) -> PackageDTO:
    try:
        result = await service.add_package_with_shipment(
            package, shipment_data, current_user.id
        )
        if not result:
            raise ValueError("Nie udało się utworzyć paczki.")
        return result
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/{package_id}", response_model=PackageDTO)
@inject
async def get_package(
    package_id: int,
    current_user: User = Depends(auth.get_current_user),
    service: IPackageService = Depends(Provide[Container.package_service]),
) -> PackageDTO:
    try:
        result = await service.get_package_by_id(package_id)
        if not result:
            raise ValueError("Paczka nie znaleziona.")
        return result
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.put("/{package_id}", response_model=PackageDTO)
@inject
async def update_package(
    package_id: int,
    data: PackageIn,
    current_user: User = Depends(auth.get_current_user),
    service: IPackageService = Depends(Provide[Container.package_service]),
) -> PackageDTO:
    try:
        result = await service.update_package(package_id, data)
        if not result:
            raise ValueError("Nie udało się zaktualizować paczki.")
        return result
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.delete("/{package_id}", response_model=PackageDTO)
@inject
async def delete_package(
    package_id: int,
    current_user: User = Depends(auth.get_current_user),
    service: IPackageService = Depends(Provide[Container.package_service]),
) -> PackageDTO:
    try:
        result = await service.delete_package(package_id)
        if not result:
            raise ValueError("Nie udało się usunąć paczki.")
        return result
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get("/", response_model=Iterable[PackageDTO])
@inject
async def get_all_packages(
    current_user: User = Depends(auth.get_current_user),
    service: IPackageService = Depends(Provide[Container.package_service]),
) -> Iterable[PackageDTO]:
    return await service.get_all_packages()
