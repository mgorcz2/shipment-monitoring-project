"""A class representing package service."""

from typing import Any, Iterable

from src.core.domain.shipment import Package, PackageIn
from src.core.repositories.ipackage import IPackageRepository
from src.infrastructure.services.ipackage import IPackageService


class PackageService(IPackageService):
    """Implementation of package service."""

    def __init__(self, repository: IPackageRepository) -> None:
        self._repository = repository

    async def add_package(self, data: PackageIn, shipment_id: int) -> Any | None:
        return await self._repository.add_package(data, shipment_id)

    async def get_package_by_id(self, package_id: int) -> Any | None:
        return await self._repository.get_package_by_id(package_id)

    async def get_all_packages(self) -> Iterable[Any]:
        return await self._repository.get_all_packages()

    async def update_package(self, package_id: int, data: PackageIn) -> Any | None:
        return await self._repository.update_package(package_id, data)

    async def delete_package(self, package_id: int) -> Any | None:
        return await self._repository.delete_package(package_id)
