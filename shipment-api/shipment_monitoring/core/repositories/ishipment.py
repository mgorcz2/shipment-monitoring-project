from abc import ABC, abstractmethod
from typing import Any, Iterable
from uuid import UUID


from shipment_monitoring.core.domain.shipment import ShipmentIn
from shipment_monitoring.core.domain.location import Location

class IShipmentRepository(ABC):

    @abstractmethod
    async def get_all_shipments(self) -> Iterable[Any]:
        '''abstract '''

    @abstractmethod
    async def get_shipment_by_id(self, shipment_id: Any) -> Any | None:
        '''abstract '''

    @abstractmethod
    async def add_shipment(self, shipment: ShipmentIn, user_id: UUID) -> Any | None:
        '''abstract '''