"""Module containing shipment repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable, Tuple
from uuid import UUID


from shipment_monitoring.core.domain.shipment import ShipmentIn, ShipmentStatus, Shipment
from shipment_monitoring.core.domain.location import Location

class IShipmentRepository(ABC):
    """An abstract class representing protocol of shipment repository."""
    
    @abstractmethod
    async def assign_shipment_to_courier(self, shipment_id: int, courier_id: UUID) -> Any | None:
        """The abstract assigning shipment to courier.

        Args:
            courier_id (int): The id of the courier.
            shipment_id (int): The id of the shipment.

        Returns:
            Any | None: The shipment details if updated.
        """    
    @abstractmethod
    async def update_status(self, courier_id: UUID, shipment_id: int, new_status: ShipmentStatus) -> Any | None:
        """The abstract changing shipment status by provided id and courier id.

        Args:
            courier_id (int): The id of the courier.
            shipment_id (int): The id of the shipment.
            new_status (ShipmentStatus): The new status.

        Returns:
            Any | None: The shipment details if updated.
        """
    
    
    @abstractmethod
    async def check_status(self, shipment_id: int, recipient_email: str) -> Any | None:
        """The abstract getting shipment by provided id and Recipient email.

        Args:
            shipment_id (int): The id of the shipment.
            recipient_email (int): The recipient_email of the shipment.

        Returns:
            Any | None: The shipment details if exists.
        """
    
    @abstractmethod
    async def get_all_shipments(self) -> Iterable[Any]:
        """The abstract getting all shipments from data storage.

        Returns:
            Iterable[Any]: Aiports in the data storage.
        """

    @abstractmethod
    async def get_shipment_by_id(self, shipment_id: int) -> Any | None:
        """The abstract getting shipment by provided id.

        Args:
            shipment_id (int): The id of the shipment.

        Returns:
            Any | None: The shipment details if exists.
        """

    @abstractmethod
    async def add_shipment(self, data: ShipmentIn, origin: str, destination: str, origin_coords: Tuple, destination_coords: Tuple, user_id: UUID) -> Any | None:
        """The abstract adding new shipment to the data storage.

        Args:
            data (ShipmentIn): The shipment input data.
            origin (str): The origin address of the shipment.
            destination (str): The destination address of the shipment.
            origin (Tuple): The origin coords of the shipment.
            destination (Tuple): The destination coords of the shipment.
            user_id (UUID): UUID of the user(sender)
            

        Returns:
            Any | None: The shipment object if created.
        """
        
    @abstractmethod
    async def update_shipment(self,
                              shipment_id: int,
                              old_shipment: Shipment,
                              data: ShipmentIn, 
                              origin: str, 
                              destination: str, 
                              origin_coords: Tuple, 
                              destination_coords: Tuple
                              ) -> Any | None:
        """The abstract updating shipment data.

        Args:
            shipment_id (int): The id of the shipment.
            old_shipment: The old shipment object.
            data (ShipmentIn): The updated shipment details.
            origin (str): The origin address of the shipment.
            destination (str): The destination address of the shipment.
            origin (Tuple): The origin coords of the shipment.
            destination (Tuple): The destination coords of the shipment.

            

        Returns:
            Any | None: The updated shipment details if updated.
        """