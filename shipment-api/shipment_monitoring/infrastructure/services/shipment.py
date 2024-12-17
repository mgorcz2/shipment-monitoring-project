"""Module containing shipment service implementation."""

from typing import Iterable, Any
from shipment_monitoring.core.domain.shipment import ShipmentStatus, ShipmentIn, Shipment
from shipment_monitoring.core.repositories.ishipment import IShipmentRepository
from shipment_monitoring.infrastructure.dto.shipmentDTO import ShipmentDTO, ShipmentWithDistanceDTO
from shipment_monitoring.infrastructure.services.ishipment import IShipmentService
from shipment_monitoring.infrastructure.external.geolocation import geopy
from shipment_monitoring.core.domain.location import Location
from uuid import UUID


class ShipmentService(IShipmentService):
    """A class representing implementation of shipment-related services."""
    _repository: IShipmentRepository

    def __init__(self, repository: IShipmentRepository) -> None:
        self._repository = repository
        
        
    async def assign_shipment_to_courier(self, shipment_id: int, courier_id: UUID) -> ShipmentDTO| None:
        """The method assigning shipment to courier in the repository.

        Args:
            courier_id (int): The id of the courier.
            shipment_id (int): The id of the shipment.

        Returns:
            ShipmentDTO | None: The shipment DTO details if updated.
        """                     
        shipment = await self._repository.assign_shipment_to_courier(shipment_id, courier_id)
        return ShipmentDTO.from_record(shipment) if shipment else None
    
    async def update_status(self, courier_id: UUID, shipment_id: int, new_status: ShipmentStatus) -> ShipmentDTO | None:
        """The method changing shipment status by provided id in the repository.
        
        Args:
            courier_id (int): The id of the courier.
            shipment_id (int): The id of the shipment.
            new_status (ShipmentStatus): The new status.

        Returns:
            ShipmentDTO | None: The shipment DTO details if updated.
        """
        shipment = await self._repository.update_status(courier_id, shipment_id, new_status)
        return ShipmentDTO.from_record(shipment) if shipment else None
        

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
    
    async def delete_shipment(self, shipment_id: int) -> dict | None:
        """The method deleting shipment by provided id.

        Args:
            shipment_id (int): The id of the shipment.

        Returns:
            dict | None: The shipment object from repository if deleted.
        """
        deleted_shipment = await self._repository.delete_shipment(shipment_id)
        return deleted_shipment if deleted_shipment else None
    
    async def get_all_shipments(self) -> Iterable[ShipmentDTO]:
        """The method getting all shipment from the repository.

        Returns:
            Iterable[ShipmentDTO]: The collection of the shipments.
        """
        shipments = await self._repository.get_all_shipments()
        return [ShipmentDTO.from_record(shipment) for shipment in shipments]

    
    async def sort_by_distance(self, courier_id: UUID, courier_location: Location) -> Iterable[ShipmentWithDistanceDTO] | None:
        """The method sorting shipments by destination distance from courier.

        Args:
            courier_location (Location): Location of courier.

        Returns:
            Iterable[ShipmentWithDistanceDTO]: Shipments with distance attribute sorted collection.
        """

        if shipments := await self._repository.get_all_shipments():
            courier_address = await geopy.get_address_from_location(courier_location)
            courier_coords = await geopy.get_coords(courier_address)
            shipmentsDTOs = [ShipmentWithDistanceDTO.from_record(shipment) 
                            for shipment in shipments 
                            if shipment.courier_id == courier_id]
        
            sorted_shipments = []
        
            for shipment in shipmentsDTOs:
                if shipment.status in ["ready_for_pickup" , "returned_to_sender"]:
                    origin_coords = shipment.origin_coords
                    shipment.origin_distance = await geopy.get_distance(courier_coords,origin_coords)
                    sorted_shipments.append(shipment)
                elif shipment.status in ["out_for_delivery", "failed_attempt"]:
                    destination_coords = shipment.destination_coords
                    shipment.destination_distance = await geopy.get_distance(courier_coords, destination_coords)
                    sorted_shipments.append(shipment)
                sorted_shipments = sorted(
                    sorted_shipments,
                    key=lambda x: x.origin_distance if x.status in ["ready_for_pickup", "returned_to_sender"]
                    else x.destination_distance
                    )
            return sorted_shipments
        return None
                
                
    async def add_shipment(self, data: ShipmentIn, user_id: UUID) -> ShipmentDTO | None:
        """The method adding a shipment to the repository.
        
        Args:
            shipment (ShipmentIn): The shipment input data.
            user_id (UUID): UUID of the user(sender).

        Returns:
            ShipmentDTO | None: The newly added shipment if added.
        """
        origin = await geopy.get_address_from_location(data.origin)
        destination = await geopy.get_address_from_location(data.destination)
        origin_coords = await geopy.get_coords(origin)
        destination_coords = await geopy.get_coords(destination)
        new_shipment = await self._repository.add_shipment(data, origin, destination, origin_coords, destination_coords, user_id)
        return ShipmentDTO.from_record(new_shipment) if new_shipment else None
        

    async def update_shipment(self, shipment_id: int, data: ShipmentIn) -> ShipmentDTO | None:
        """The method updating shipment data in the reposistory.

        Args:
            shipment_id (int): The id of the shipment.
            data (ShipmentIn): The updated shipment details.

        Returns:
            ShipmentDTO | None: The updated shipment DTO details if updated.
        """
        origin = await geopy.get_address_from_location(data.origin)
        destination = await geopy.get_address_from_location(data.destination)
        origin_coords = await geopy.get_coords(origin)
        destination_coords = await geopy.get_coords(destination)
        if old_shipment := await self._repository.get_shipment_by_id(shipment_id):
            shipment = await self._repository.update_shipment(shipment_id, old_shipment, data, origin, destination, origin_coords, destination_coords)
            return ShipmentDTO.from_record(shipment) if shipment else None
        return None