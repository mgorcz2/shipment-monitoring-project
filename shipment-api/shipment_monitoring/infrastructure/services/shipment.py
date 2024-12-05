from typing import Iterable
from shipment_monitoring.core.domain.shipment import Shipment
from shipment_monitoring.core.repositories.ishipment import IShipmentRepository
from shipment_monitoring.infrastructure.dto.shipmentDTO import ShipmentDTO
from shipment_monitoring.core.domain.shipment import ShipmentIn
from shipment_monitoring.infrastructure.services.ishipment import IShipmentService
from shipment_monitoring.infrastructure.external.geopy import geopy

class ShipmentService(IShipmentService):
    _repository: IShipmentRepository

    def __init__(self, repository: IShipmentRepository) -> None:
        self._repository = repository

    async def get_all_shipments(self) -> Iterable[ShipmentDTO]:
        return await self._repository.get_all_shipments()

    async def get_shipment_by_id(self, shipment_id: int) -> ShipmentDTO | None:
        shipment = await self._repository.get_by_id(shipment_id)
        return ShipmentDTO.from_record(shipment)

    async def add_shipment(self, data: ShipmentIn) -> ShipmentDTO | None:
        origin_address = f"{data.origin.street}, {data.origin.street_number}, {data.origin.city}, {data.origin.postcode}"
        origin_coords = await geopy.get_coordinates(origin_address)
        
        destination_address = f"{data.destination.street}, {data.destination.street_number}, {data.destination.city}, {data.destination.postcode}"
        destination_coords = await geopy.get_coordinates(destination_address)
        
        if not origin_coords or not destination_coords:
            raise ValueError("Invalid origin or destination address")
        new_shipment = await self._repository.add_shipment(data, origin_coords, destination_coords)
        return ShipmentDTO.from_record(dict(new_shipment))
        
