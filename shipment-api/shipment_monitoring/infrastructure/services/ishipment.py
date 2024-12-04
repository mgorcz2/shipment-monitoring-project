from abc import ABC, abstractmethod
from typing import Iterable

from shipment_monitoring.core.domain.shipment import ShipmentIn, Shipment
from shipment_monitoring.infrastructure.dto.shipmentDTO import ShipmentDTO

class IShipmentService(ABC):
    @abstractmethod
    async def get_shipment_by_id(self, shipment_id: int) -> Shipment | None:
        pass

    @abstractmethod
    async def get_all_shipments(self) -> Iterable[Shipment]:
        pass

    @abstractmethod
    async def add_shipment(self, shipment: ShipmentIn) -> ShipmentDTO | None:
        pass