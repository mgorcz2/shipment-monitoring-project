"""Module containing shipment repository implementation."""

from typing import Any, Iterable, Tuple
from uuid import UUID

from sqlalchemy import select, join

from shipment_monitoring.core.repositories.ishipment import IShipmentRepository
from shipment_monitoring.core.domain.shipment import Shipment, ShipmentIn
from shipment_monitoring.db import (
    shipment_table, 
    database
)


class ShipmentRepository(IShipmentRepository):
    """A class representing shipment DB repository."""
    
    async def check_status(self, shipment_id: int, recipient_email: str) -> Any | None:
        """The method getting shipment by provided id and Recipient email from the data storage.

        Args:
            shipment_id (int): The id of the shipment.
            recipient_email (int): The recipient_email of the shipment.

        Returns:
            Any | None: The shipment details if exists.
        """
        query = (
                select(shipment_table)
                .where (
                    (shipment_table.c.id == shipment_id) &
                    (shipment_table.c.recipient_email == recipient_email)
                )
        )
        shipment = await database.fetch_one(query)
        return shipment

    
    async def get_all_shipments(self) -> Iterable[Any]:
        """The method getting all shipments from the data storage.

        Returns:
            Iterable[Any]: Shipments in the data storage.
        """
        query = select(shipment_table)
        shipments = await database.fetch_all(query)
        return shipments
    
    async def get_shipment_by_id(self, shipment_id: int) -> Any | None:
        """The method getting shipment by provided id.

        Args:
            shipment_id (int): The id of the shipment.

        Returns:
            Any | None: The shipment details if exists.
        """

        query = (
                select(shipment_table)
                .where (shipment_table.c.id == shipment_id)
        )
        shipment = await database.fetch_one(query)
        return shipment if shipment else None

    async def add_shipment(self, data: ShipmentIn, origin: str, destination: str, origin_coords: Tuple, destination_coords: Tuple, user_id: UUID) -> Shipment | None:
        """The method adding new shipment to the data storage.

        Args:
            data (ShipmentIn): The shipment input data.
            origin (str): The origin address of the shipment.
            destination (str): The destination address of the shipment.
            origin (Tuple): The origin coords of the shipment.
            destination (Tuple): The destination coords of the shipment.
            user_id (UUID): UUID of the user(sender)

        Returns:
            Shipment | None: The shipment object if created.
        """
        query = shipment_table.insert().values(
            sender_id=user_id,
            status="ready_for_pickup",
            weight = data.weight,
            recipient_email = None if "" else data.recipient_email,
            origin=origin,
            destination=destination,
            origin_latitude = origin_coords[0],
            origin_longitude = origin_coords[1],
            destination_latitude = destination_coords[0],
            destination_longitude = destination_coords[1]
            )
        new_shipment_id = await database.execute(query)
        new_shipment = await self.get_shipment_by_id(new_shipment_id)
        return new_shipment if new_shipment else None
