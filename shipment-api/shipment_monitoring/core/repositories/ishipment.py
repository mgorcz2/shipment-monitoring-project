from abc import ABC, abstractmethod
from typing import Any, Iterable

from shipment_monitoring.core.domain.shipment import ShipmentIn

class IShipmentRepository(ABC):

    @abstractmethod
    async def get_all_shipments(self) -> Iterable[Any]:
        '''abstract '''

    @abstractmethod
    async def get_by_id(self, shipment_id: Any) -> Any | None:
        '''abstract '''