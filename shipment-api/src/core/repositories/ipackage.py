"""Module containing package repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from src.core.domain.shipment import Package, PackageIn


class IPackageRepository(ABC):
    """An abstract class representing protocol of package repository."""

    @abstractmethod
    async def add_package(self, data: PackageIn, shipment_id: int) -> Any | None:
        """Add a new package to the data storage.

        Args:
            data (PackageIn): The package input data.

        Returns:
            Any | None: The package object if created.
        """

    @abstractmethod
    async def get_package_by_id(self, package_id: int) -> Any | None:
        """Get package by provided id (shipment_id).

        Args:
            package_id (int): The id of the package (shipment_id).

        Returns:
            Any | None: The package details if exists.
        """

    @abstractmethod
    async def get_all_packages(self) -> Iterable[Any]:
        """Get all packages from data storage.

        Returns:
            Iterable[Any]: Packages in the data storage.
        """

    @abstractmethod
    async def update_package(self, package_id: int, data: PackageIn) -> Any | None:
        """Update package data.

        Args:
            package_id (int): The id of the package (shipment_id).
            data (PackageIn): The updated package details.

        Returns:
            Any | None: The updated package details if updated.
        """

    @abstractmethod
    async def delete_package(self, package_id: int) -> Any | None:
        """Delete package by provided id (shipment_id).

        Args:
            package_id (int): The id of the package (shipment_id).

        Returns:
            Any | None: The package details if deleted.
        """
