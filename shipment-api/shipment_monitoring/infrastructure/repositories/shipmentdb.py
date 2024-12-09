from typing import Any, Iterable, Tuple

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join

from shipment_monitoring.core.repositories.ishipment import IShipmentRepository
from shipment_monitoring.core.domain.shipment import Shipment, ShipmentIn
from shipment_monitoring.db import (
    shipment_table, database
)
from shipment_monitoring.infrastructure.dto.shipmentDTO import ShipmentDTO, ShipmentWithDistanceDTO


class ShipmentRepository(IShipmentRepository):
    async def get_all_shipments(self) -> Iterable[Any]:
        query = select(shipment_table)
        shipments = await database.fetch_all(query)
        return shipments
    
    async def get_shipment_by_id(self, shipment_id: Any) -> Any | None:

        query = (
            select(shipment_table)
            .where (shipment_table.c.id == shipment_id)
        )
        shipment = await database.fetch_one(query)
        return shipment if shipment else None

    async def add_shipment(self, data: ShipmentIn, origin, destination) -> Shipment | None:   #sender create shipment so default status is ready for pickup
        query = shipment_table.insert().values(
            status="ready_for_pickup",  
            origin=origin,
            destination=destination,
            weight=data.weight
            )
        new_shipment_id = await database.execute(query)
        new_shipment = await self.get_shipment_by_id(new_shipment_id)
        return new_shipment if new_shipment else None
