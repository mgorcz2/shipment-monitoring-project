"""Module containing shipment repository implementation."""

from typing import Any, Iterable, Tuple
from uuid import UUID

from sqlalchemy import delete, join, select, update

from src.core.domain.shipment import (
    Shipment,
    ShipmentIn,
    ShipmentStatus,
)
from src.core.repositories.ishipment import IShipmentRepository
from src.db import database, shipment_table


class ShipmentRepository(IShipmentRepository):
    """A class representing shipment DB repository."""

    async def assign_shipment_to_courier(
        self, shipment_id: int, courier_id: UUID
    ) -> Any | None:
        """The method assigning shipment to courier in the data storage.

        Args:
            courier_id (int): The id of the courier.
            shipment_id (int): The id of the shipment.

        Returns:
            Any | None: The shipment details if updated.
        """

        query = (
            update(shipment_table)
            .where(shipment_table.c.id == shipment_id)
            .values(courier_id=courier_id)
            .returning(shipment_table)
        )
        shipment = await database.fetch_one(query)
        return shipment

    async def update_status(
        self, courier_id: UUID, shipment_id: int, new_status: ShipmentStatus
    ) -> Any | None:
        """The method changing shipment status by provided id in the data storage.

        Args:
            courier_id (int): The id of the courier.
            shipment_id (int): The id of the shipment.
            new_status (ShipmentStatus): The new status.

        Returns:
            Any | None: The shipment details if updated.
        """
        query = (
            update(shipment_table)
            .where(
                (shipment_table.c.id == shipment_id)
                & (shipment_table.c.courier_id == courier_id)
            )
            .values(status=new_status)
            .returning(shipment_table)
        )
        shipment = await database.fetch_one(query)
        return shipment

    async def check_status(self, shipment_id: int, recipient_email: str) -> Any | None:
        """The method getting shipment by provided id and Recipient email from the data storage.

        Args:
            shipment_id (int): The id of the shipment.
            recipient_email (int): The recipient_email of the shipment.

        Returns:
            Any | None: The shipment details if exists.
        """
        query = select(shipment_table).where(
            (shipment_table.c.id == shipment_id)
            & (shipment_table.c.recipient_email == recipient_email)
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

        query = select(shipment_table).where(shipment_table.c.id == shipment_id)
        shipment = await database.fetch_one(query)
        return shipment if shipment else None

    async def delete_shipment(self, shipment_id: int) -> Any | None:
        """The method deleting shipment by provided id.

        Args:
            shipment_id (int): The id of the shipment.

        Returns:
            Any | None: The shipment object from database if deleted.
        """
        query = (
            delete(shipment_table)
            .where(shipment_table.c.id == shipment_id)
            .returning(shipment_table)
        )
        deleted_shipment = await database.fetch_one(query)
        return deleted_shipment if deleted_shipment else None

    async def add_shipment(
        self,
        data: ShipmentIn,
        origin: str,
        destination: str,
        origin_coords: Tuple,
        destination_coords: Tuple,
        user_id: UUID,
    ) -> Any | None:
        """The method adding new shipment to the data storage.

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
        query = shipment_table.insert().values(
            sender_id=user_id,
            status="ready_for_pickup",
            recipient_email=(
                None if data.recipient_email == "" else data.recipient_email
            ),
            origin=origin,
            destination=destination,
            origin_latitude=origin_coords[0],
            origin_longitude=origin_coords[1],
            destination_latitude=destination_coords[0],
            destination_longitude=destination_coords[1],
        )
        new_shipment_id = await database.execute(query)
        new_shipment = await self.get_shipment_by_id(new_shipment_id)
        return new_shipment if new_shipment else None

    async def update_shipment(
        self,
        shipment_id: int,
        old_shipment: Shipment,
        data: ShipmentIn,
        origin: str,
        destination: str,
        origin_coords: Tuple,
        destination_coords: Tuple,
    ) -> Any | None:
        """The method updating shipment data in the data storage.

        Args:
            shipment_id (int): The id of the shipment.
            old_shipment: The old shipment object.
            data (ShipmentIn): The updated shipment details.
            origin (str): The origin address of the shipment.
            destination (str): The destination address of the shipment.
            origin (Tuple): The origin coords of the shipment.
            destination (Tuple): The destination coords of the shipment.

        Returns:
            Any | None: The updated shipment if updated.
        """
        query = (
            update(shipment_table)
            .where(shipment_table.c.id == shipment_id)
            .values(
                sender_id=old_shipment.sender_id,
                courier_id=old_shipment.courier_id,
                status=old_shipment.status,
                weight=data.weight,
                recipient_email=(
                    None if data.recipient_email == "" else data.recipient_email
                ),
                origin=origin,
                destination=destination,
                origin_latitude=origin_coords[0],
                origin_longitude=origin_coords[1],
                destination_latitude=destination_coords[0],
                destination_longitude=destination_coords[1],
            )
            .returning(shipment_table)
        )
        shipment = await database.fetch_one(query)
        return shipment if shipment else None
