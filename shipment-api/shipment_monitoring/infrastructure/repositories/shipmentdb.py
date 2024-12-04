from typing import Any, Iterable, Tuple

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join

from shipment_monitoring.core.repositories.ishipment import IShipmentRepository
from shipment_monitoring.core.domain.shipment import Shipment, ShipmentIn
from shipment_monitoring.db import (
    shipment_table, database
)
from shipment_monitoring.infrastructure.dto.shipmentDTO import ShipmentDTO


class ShipmentRepository(IShipmentRepository):
    async def get_all_shipments(self) -> Iterable[Any]:
        query = select(shipment_table)
        shipments = await database.fetch_all(query)
        return [ShipmentDTO.from_record(shipment) for shipment in shipments]

    async def get_by_id(self, shipment_id: Any) -> Any | None:

        query = (
            select(shipment_table)
            .where (shipment_table.c.id == shipment_id)
        )
        shipment = await database.fetch_one(query)
        return ShipmentDTO.from_record(shipment) if shipment else None

    async def add_shipment(self, data: ShipmentIn, origin_cords: Tuple[float, float], destination_coords: Tuple[float, float]) -> Any | None:
        query = shipment_table.insert().values(
            status=data.status,
            origin_latitude=origin_cords[0],
            origin_longitude=origin_cords[1],
            destination_latitude=destination_coords[0],
            destination_longitude=destination_coords[1],
            weight=data.weight,
            )
        print(query)
        new_shipment_id = await database.execute(query)
        new_shipment = await self.get_by_id(new_shipment_id)
        return new_shipment if new_shipment else None
