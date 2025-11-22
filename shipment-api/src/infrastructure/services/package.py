"""A class representing package service."""

from typing import Any, Iterable
from uuid import UUID

from src.core.domain.shipment import Package, PackageIn, ShipmentIn
from src.core.repositories.ipackage import IPackageRepository
from src.db import database
from src.infrastructure.external.email.email_service import EmailService
from src.infrastructure.services.ipackage import IPackageService
from src.infrastructure.services.ishipment import IShipmentService


class PackageService(IPackageService):
    """Implementation of package service."""

    def __init__(
        self, repository: IPackageRepository, shipment_service: IShipmentService
    ) -> None:
        self._repository = repository
        self._shipment_service = shipment_service
        self._email_service = EmailService()

    async def add_package_with_shipment(
        self, data: PackageIn, shipment_data: ShipmentIn, user_id: UUID
    ) -> Any | None:
        async with database.transaction():
            try:
                shipment = await self._shipment_service.add_shipment(
                    shipment_data, user_id
                )
            except Exception as e:
                raise ValueError(f"Shipment add failed: {str(e)}")
            package = await self._repository.add_package(data, shipment.id)
            if not package:
                raise ValueError("Failed to add package. Try again later.")
            try:
                if shipment_data.recipient_email:
                    await self._email_service.send_package_created_email(
                        shipment_data.recipient_email, shipment.id
                    )
            except Exception as e:
                print(f"Email sending failed: {str(e)}")
            return package

    async def get_package_by_id(self, package_id: int) -> Any | None:
        return await self._repository.get_package_by_id(package_id)

    async def get_all_packages(self) -> Iterable[Any]:
        return await self._repository.get_all_packages()

    async def update_package(self, package_id: int, data: Package) -> Any | None:
        return await self._repository.update_package(package_id, data)

    async def delete_package(self, package_id: int) -> Any | None:
        return await self._repository.delete_package(package_id)
