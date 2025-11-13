"""Module containing package service abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable
from uuid import UUID

from src.core.domain.shipment import Package, PackageIn, ShipmentIn
from src.infrastructure.dto.shipmentDTO import PackageDTO


class IPackageService(ABC):
    """An abstract class representing protocol of package service."""

    @abstractmethod
    async def add_package_with_shipment(
        self, data: PackageIn, shipment_data: ShipmentIn, user_id: UUID
    ) -> PackageDTO | None:
        """Add a new package to the data storage."""

    @abstractmethod
    async def get_package_by_id(self, package_id: int) -> PackageDTO | None:
        """Get package by provided id (shipment_id)."""

    @abstractmethod
    async def get_all_packages(self) -> Iterable[Any]:
        """Get all packages from data storage."""

    @abstractmethod
    async def update_package(
        self, package_id: int, data: PackageIn
    ) -> PackageDTO | None:
        """Update package data."""

    @abstractmethod
    async def delete_package(self, package_id: int) -> PackageDTO | None:
        """Delete package by provided id (shipment_id)."""
