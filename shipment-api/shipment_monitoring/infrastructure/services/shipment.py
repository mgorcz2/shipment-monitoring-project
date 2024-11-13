from typing import Iterable, Any

from shipment_monitoring.core.domain.shipment import Shipment
from shipment_monitoring.core.repositories.ishipment import IShipmentRepository
from shipment_monitoring.infrastructure.dto.shipment import ShipmentDTO
from shipment_monitoring.infrastructure.services.ishipment import IShipmentService

class ShipmentService(IShipmentService):
    _repository: IShipmentRepository

    def __init__(self, repository: IShipmentRepository) -> None:
        self._repository = repository

    async def get_all_shipments(self) -> Iterable[ShipmentDTO]:
        return await self._repository.get_all_shipments()

    async def get_shipment_by_id(self, shipment_id: int) -> ShipmentDTO | None:
        return await self._repository.get_by_id(shipment_id)

    async def add_shipment(self, shipment: ShipmentDTO) -> ShipmentDTO | None:
        return await self._repository.add_shipment(shipment)
