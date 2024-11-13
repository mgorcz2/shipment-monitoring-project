from abc import ABC, abstractmethod
from typing import Iterable

from shipment_monitoring.core.domain.shipment import ShipmentIn, Shipment

class IShipmentService(ABC):
    @abstractmethod
    async def get_shipment_by_id(self, shipment_id: int) -> Shipment | None:
        pass

    async def get_all_shipments(self) -> Iterable[Shipment]:
        pass