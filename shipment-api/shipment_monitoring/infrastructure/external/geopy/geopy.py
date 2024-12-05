from geopy.geocoders import Nominatim
from typing import Tuple, Optional

geolocator = Nominatim(user_agent="shipment_app", timeout=200)
async def get_coordinates(address: str) -> Optional[Tuple[float, float]]:
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    return None

def get_address(latitude: float, longitude: float) -> str | None:
    location = geolocator.reverse([latitude, longitude])
    if location:
        address = location.raw.get('address', {})
        street = address.get('road', 'N/A')
        street_number = address.get('house_number', 'N/A')  # Numer ulicy
        postal_code = address.get('postcode', 'N/A')
        city = address.get('city', 'N/A')
        
        return f"Ulica: {street} {street_number}, Miejscowość: {city}, Kod pocztowy: {postal_code}".strip()
    return None

