"""Module containing shipment service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from shipment_monitoring.core.domain.shipment import ShipmentIn, Shipment
from shipment_monitoring.core.domain.location import Location
from shipment_monitoring.infrastructure.dto.shipmentDTO import ShipmentDTO, ShipmentWithDistanceDTO
from uuid import UUID

class IShipmentService(ABC):
    """An abstract class representing protocol of shipment service."""
    
    @abstractmethod
    async def get_shipment_by_id(self, shipment_id: int) -> ShipmentDTO | None:
        """The abstract getting shipment by provided id.

        Args:
            shipment_id (int): The id of the shipment.

        Returns:
            ShipmentDTO | None: The shipment DTO details if exists.
        """

    @abstractmethod
    async def get_all_shipments(self) -> Iterable[ShipmentDTO]:
        """The abstract getting all shipment from the repository.

        Returns:
            Iterable[ShipmentDTO]: The collection of the shipments.
        """
    @abstractmethod
    async def add_shipment(self, shipment: ShipmentIn, user_id: UUID) -> ShipmentDTO | None:
        """The abstract adding a shipment to the repository.
        Args:
            shipment (ShipmentIn): The shipment input data.
            user_id (UUID): UUID of the user(sender).

        Returns:
            ShipmentDTO | None: The newly added shipment if added.
        """
    @abstractmethod
    async def sort_by_distance(self, courier_location: Location, keyword: str) -> Iterable[ShipmentWithDistanceDTO]:
        """The abstract sorting shipments by destination distance from courier.

        Args:
            courier_location (Location): Location of courier.
            keyword (str): Sorting key.

        Returns:
            Iterable[ShipmentWithDistanceDTO]: Shipments with distance attribute sorted collection.
        """

  