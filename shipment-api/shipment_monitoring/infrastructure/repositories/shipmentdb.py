from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join

from shipment_monitoring.core.repositories.ishipment import IShipmentRepository
from shipment_monitoring.core.domain.shipment import Shipment, ShipmentIn
from shipment_monitoring.db import (
    shipment_table, database
)
from shipment_monitoring.infrastructure.dto.shipment import ShipmentDTO

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
