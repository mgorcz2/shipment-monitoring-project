"""A module containing geolocation methods."""

from geopy.geocoders import Nominatim
from typing import Tuple, Optional
from geopy.distance import geodesic
from shipment_monitoring.core.domain.location import Location
from haversine import haversine


geolocator = Nominatim(user_agent="shipment_app", timeout=1000)

async def get_address(location: str) -> str:
    """Geocode a location string to standarized address.

    Args:
        location (str): A location string.

    Raises:
        ValueError: If location cannot be found.

    Returns:
        str: Formatted address.
    """
    address = geolocator.geocode(location)
    if not address:
        raise ValueError(f"Address not found: {location}")
    return str(address)

async def get_address_from_location(location: Location) -> str:
    """Getting a full adress from a Location object.

    Args:
        location (Location): A Location object.

    Returns:
        str: Formatted address.
    """
    location = f"{location.street}, {location.street_number}, {location.city}, {location.postcode}"
    return await get_address(location)

async def get_coords(address: str) -> tuple[float,float] | None:
    """Convert an adress to coordinates.

    Args:
        address (str): A location address to be converted to coordinates.

    Returns:
        tuple[float,float]: A tuple of (latitude, longitude) of None if cannot be found.
    """
    location = geolocator.geocode(address)
    return (location.latitude, location.longitude) or None

async def get_distance(courier_coords: tuple[float, float],shipment_coords: tuple[float,float]) -> float:
    """Calculate the distance between two geographical coordinates.

    Args:
        courier_coords (tuple[float, float]): Latitude and longitude of the courier.
        shipment_coords (tuple[float,float]): Latitude and longitude of the shipment.

    Returns:
        float: Distance between the two points in kilometers, rounded to two decimal places.
    """
    return round(haversine(courier_coords, shipment_coords), 2)