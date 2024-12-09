from geopy.geocoders import Nominatim
from typing import Tuple, Optional
from geopy.distance import geodesic
from shipment_monitoring.core.domain.location import Location


geolocator = Nominatim(user_agent="shipment_app", timeout=200)
async def get_address(location: str) -> str:
    address = geolocator.geocode(location)
    if not address:
        raise ValueError(f"Address not found: {location}")
    return str(address)

async def get_address_from_location(location: Location) -> str:
    location = f"{location.street}, {location.street_number}, {location.city}, {location.postcode}"
    return await get_address(location)

async def get_coords(address: str) -> tuple[float,float]:
    location = geolocator.geocode(address)
    return (location.latitude, location.longitude) or None

async def get_distance(courier_coords: tuple[float, float],shipment_coords: tuple[float,float]):
    return geodesic(courier_coords, shipment_coords).kilometers