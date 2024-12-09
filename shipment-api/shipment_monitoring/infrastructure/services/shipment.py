from typing import Iterable, Any
from shipment_monitoring.core.domain.shipment import Shipment
from shipment_monitoring.core.repositories.ishipment import IShipmentRepository
from shipment_monitoring.infrastructure.dto.shipmentDTO import ShipmentDTO, ShipmentWithDistanceDTO
from shipment_monitoring.core.domain.shipment import ShipmentIn
from shipment_monitoring.infrastructure.services.ishipment import IShipmentService
from shipment_monitoring.infrastructure.external.geopy import geopy
from shipment_monitoring.core.domain.location import Location
class ShipmentService(IShipmentService):
    _repository: IShipmentRepository

    def __init__(self, repository: IShipmentRepository) -> None:
        self._repository = repository

    async def get_all_shipments(self) -> Iterable[ShipmentDTO]:
        shipments = await self._repository.get_all_shipments()
        return [ShipmentDTO.from_record(shipment) for shipment in shipments]

    
    async def sort_by_distance(self, courier_location: Location) -> Iterable[ShipmentWithDistanceDTO]:
        shipments = await self._repository.get_all_shipments()
        courier_address = await geopy.get_address_from_location(courier_location)
        courier_coords = await geopy.get_coords(courier_address)
        
        shipments_dtos=[]
        for shipment in shipments:
            shipment_coords = await geopy.get_coords(shipment.origin)
            distance = await geopy.get_distance(courier_coords,shipment_coords)
            shipment_dto = ShipmentWithDistanceDTO.from_record(shipment)
            shipment_dto.distance = distance
            shipments_dtos.append(shipment_dto)
            
        sorted_shipments = sorted(shipments_dtos, key=lambda x: x.distance)
        
        return sorted_shipments
            
    
    async def get_shipment_by_id(self, shipment_id: int) -> ShipmentDTO | None:
        shipment = await self._repository.get_shipment_by_id(shipment_id)
        return ShipmentDTO.from_record(shipment)

    async def add_shipment(self, data: ShipmentIn) -> ShipmentDTO | None:
        origin= await geopy.get_address_from_location(data.origin)
        destination = await geopy.get_address_from_location(data.destination)
        new_shipment = await self._repository.add_shipment(data, origin, destination)
        return ShipmentDTO.from_record(dict(new_shipment))
        
