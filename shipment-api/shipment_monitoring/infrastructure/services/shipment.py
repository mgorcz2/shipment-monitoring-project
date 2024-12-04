from typing import Iterable, Any, Optional
from shipment_monitoring.core.domain.shipment import Shipment
from shipment_monitoring.core.repositories.ishipment import IShipmentRepository
from shipment_monitoring.infrastructure.dto.shipmentDTO import ShipmentDTO
from shipment_monitoring.core.domain.shipment import ShipmentIn
from shipment_monitoring.infrastructure.services.ishipment import IShipmentService



from geopy.geocoders import Nominatim
from typing import Tuple

geolocator = Nominatim(user_agent="shipment_app")
async def get_coordinates(address: str) -> Optional[Tuple[float, float]]:
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    return None



class ShipmentService(IShipmentService):
    _repository: IShipmentRepository

    def __init__(self, repository: IShipmentRepository) -> None:
        self._repository = repository

    async def get_all_shipments(self) -> Iterable[ShipmentDTO]:
        return await self._repository.get_all_shipments()

    async def get_shipment_by_id(self, shipment_id: int) -> ShipmentDTO | None:
        return await self._repository.get_by_id(shipment_id)

    async def add_shipment(self, data: ShipmentIn) -> ShipmentDTO | None:
        origin_address = f"{data.origin_street}, {data.origin_street_number}, {data.origin_city}, {data.origin_postcode}"
        origin_coords = await get_coordinates(origin_address)
        
        destination_address = f"{data.destination_street}, {data.destination_street_number}, {data.destination_city}, {data.destination_postcode}"
        destination_coords = await get_coordinates(destination_address)
        
        if not origin_coords or not destination_coords:
            raise ValueError("Invalid origin or destination address")
        new_shipment = await self._repository.add_shipment(data, origin_coords, destination_coords)
        return ShipmentDTO.from_record(dict(new_shipment))
        
