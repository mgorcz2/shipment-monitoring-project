from geopy.geocoders import Nominatim
from typing import Tuple, Optional

geolocator = Nominatim(user_agent="shipment_app", timeout=200)
async def get_coordinates(address: str) -> Optional[Tuple[float, float]]:
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    return None

def get_address(latitude: float, longitude: float) -> str | None:
    location = str(geolocator.reverse([latitude, longitude]))
    if location:
        address = location.split(',')
        return ", ".join(address[i].strip() for i in [1,0,2,6])
    return None

