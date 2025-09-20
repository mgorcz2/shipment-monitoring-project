"""Router for package endpoints."""

from typing import Iterable
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from src.container import Container
from src.core.domain.shipment import Package, PackageIn
from src.infrastructure.dto.shipmentDTO import PackageDTO
from src.infrastructure.services.ipackage import IPackageService

router = APIRouter(
    prefix="/packages",
    tags=["packages"],
)


@router.post("/", response_model=PackageDTO, status_code=status.HTTP_201_CREATED)
@inject
async def create_package(
    package: PackageIn,
    shipment_id: int,
    service: IPackageService = Depends(Provide[Container.package_service]),
) -> PackageDTO:
    try:
        result = await service.add_package(package, shipment_id)
        if not result:
            raise ValueError("Nie udało się utworzyć paczki.")
        return result
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/{package_id}", response_model=PackageDTO)
@inject
async def get_package(
    package_id: int,
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
    service: IPackageService = Depends(Provide[Container.package_service]),
) -> Iterable[PackageDTO]:
    return await service.get_all_packages()
