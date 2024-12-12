"""Module containing shipment service implementation."""

from typing import Iterable, Any
from shipment_monitoring.core.domain.shipment import Shipment
from shipment_monitoring.core.repositories.ishipment import IShipmentRepository
from shipment_monitoring.infrastructure.dto.shipmentDTO import ShipmentDTO, ShipmentWithDistanceDTO
from shipment_monitoring.core.domain.user import User
from shipment_monitoring.core.domain.shipment import ShipmentIn
from shipment_monitoring.infrastructure.services.ishipment import IShipmentService
from shipment_monitoring.infrastructure.external.geolocation import geopy
from shipment_monitoring.core.domain.location import Location
from uuid import UUID


class ShipmentService(IShipmentService):
    """A class representing implementation of shipment-related services."""
    _repository: IShipmentRepository

    def __init__(self, repository: IShipmentRepository) -> None:
        self._repository = repository

    async def check_status(self, shipment_id: int, recipient_email: str) -> ShipmentDTO | None:
        """The method getting shipment by provided id and Recipient email from the repository.

        Args:
            shipment_id (int): The id of the shipment.
            recipient_email (str): The email of the Recipient.

        Returns:
            ShipmentDTO | None: The shipment DTO details if exists.
        """
        shipment = await self._repository.check_status(shipment_id, recipient_email)
        return ShipmentDTO.from_record(shipment) if shipment else None
    

    async def get_shipment_by_id(self, shipment_id: int) -> ShipmentDTO | None:
        """The method getting shipment by provided id.

        Args:
            shipment_id (int): The id of the shipment.

        Returns:
            ShipmentDTO | None: The shipment DTO details if exists.
        """
        shipment = await self._repository.get_shipment_by_id(shipment_id)
        return ShipmentDTO.from_record(shipment) if shipment else None
    
    async def get_all_shipments(self) -> Iterable[ShipmentDTO]:
        """The method getting all shipment from the repository.

        Returns:
            Iterable[ShipmentDTO]: The collection of the shipments.
        """
        shipments = await self._repository.get_all_shipments()
        return [ShipmentDTO.from_record(shipment) for shipment in shipments]

    
    async def sort_by_distance(self, courier_location: Location, keyword) -> Iterable[ShipmentWithDistanceDTO]:
        """The method sorting shipments by destination distance from courier.

        Args:
            courier_location (Location): Location of courier.
            keyword (str): Sorting key.

        Returns:
            Iterable[ShipmentWithDistanceDTO]: Shipments with distance attribute sorted collection.
        """

        shipments = await self._repository.get_all_shipments()
        courier_address = await geopy.get_address_from_location(courier_location)
        courier_coords = await geopy.get_coords(courier_address)
        shipmentsDTOs = [ShipmentWithDistanceDTO.from_record(shipment) for shipment in shipments]
        
        for shipment in shipmentsDTOs:
            origin_coords = shipment.origin_coords
            destination_coords = shipment.destination_coords
            shipment.origin_distance = await geopy.get_distance(courier_coords,origin_coords)
            shipment.destination_distance = await geopy.get_distance(courier_coords, destination_coords)
        if keyword is "origin":
            sorted_shipments = sorted(shipmentsDTOs, key=lambda x: x.origin_distance)
        else:
            sorted_shipments = sorted(shipmentsDTOs, key=lambda x: x.destination_distance)
        return sorted_shipments
    
    async def add_shipment(self, data: ShipmentIn, user_id: UUID) -> ShipmentDTO | None:
        """The method adding a shipment to the repository.
        
        Args:
            shipment (ShipmentIn): The shipment input data.
            user_id (UUID): UUID of the user(sender).

        Returns:
            ShipmentDTO | None: The newly added shipment if added.
        """
        origin= await geopy.get_address_from_location(data.origin)
        destination = await geopy.get_address_from_location(data.destination)
        origin_coords = await geopy.get_coords(origin)
        destination_coords = await geopy.get_coords(destination)
        new_shipment = await self._repository.add_shipment(data, origin, destination, origin_coords, destination_coords, user_id)
        return ShipmentDTO.from_record(new_shipment) if new_shipment else None
        
