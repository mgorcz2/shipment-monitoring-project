"""Module containing shipment repository implementation."""

from typing import Any, Iterable, Tuple
from uuid import UUID

from sqlalchemy import delete, func, select, update
from sqlalchemy.sql import literal_column

from src.core.domain.shipment import (
    Shipment,
    ShipmentIn,
    ShipmentStatus,
)
from src.core.repositories.ishipment import IShipmentRepository
from src.db import client_table, database, shipment_table, user_table


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
        recipient_user = user_table.alias("recipient_user")
        recipient_client = client_table.alias("recipient_client")

        sender_fullname = func.concat_ws(
            literal_column("' '"),
            client_table.c.first_name,
            client_table.c.last_name,
        ).label("sender_fullname")

        recipient_fullname = func.concat_ws(
            literal_column("' '"),
            recipient_client.c.first_name,
            recipient_client.c.last_name,
        ).label("recipient_fullname")

        query = (
            select(
                shipment_table,
                sender_fullname,
                recipient_fullname,
            )
            .select_from(
                shipment_table.outerjoin(
                    user_table, shipment_table.c.sender_id == user_table.c.id
                )
                .outerjoin(client_table, user_table.c.id == client_table.c.id)
                .outerjoin(
                    recipient_user, shipment_table.c.recipient_id == recipient_user.c.id
                )
                .outerjoin(
                    recipient_client, recipient_user.c.id == recipient_client.c.id
                )
            )
            .where(
                (shipment_table.c.id == shipment_id)
                & (shipment_table.c.recipient_email == recipient_email)
            )
        )
        shipment = await database.fetch_one(query)
        return shipment

    async def get_all_shipments(self) -> Iterable[Any]:
        """The method getting all shipments from the data storage."""
        recipient_user = user_table.alias("recipient_user")
        recipient_client = client_table.alias("recipient_client")

        sender_fullname = func.concat_ws(
            literal_column("' '"),
            client_table.c.first_name,
            client_table.c.last_name,
        ).label("sender_fullname")

        recipient_fullname = func.concat_ws(
            literal_column("' '"),
            recipient_client.c.first_name,
            recipient_client.c.last_name,
        ).label("recipient_fullname")

        query = select(
            shipment_table,
            sender_fullname,
            recipient_fullname,
        ).select_from(
            shipment_table.outerjoin(
                user_table, shipment_table.c.sender_id == user_table.c.id
            )
            .outerjoin(client_table, user_table.c.id == client_table.c.id)
            .outerjoin(
                recipient_user, shipment_table.c.recipient_id == recipient_user.c.id
            )
            .outerjoin(recipient_client, recipient_user.c.id == recipient_client.c.id)
        )

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
            status="pending",
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
                recipient_id=data.recipient_id,
                courier_id=old_shipment.courier_id,
                status=old_shipment.status,
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
