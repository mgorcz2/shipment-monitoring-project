"""Data for testing"""

from shipment_monitoring.core.domain.location import Location
from shipment_monitoring.core.domain.shipment import ShipmentIn, ShipmentStatus
from shipment_monitoring.core.domain.user import UserIn, UserRole

Warszawa = Location(street="", street_number="", city="Warszawa", postcode="")
Olsztyn = Location(street="", street_number="", city="Olsztyn", postcode="")
Poznan = Location(street="", street_number="", city="Poznan", postcode="")
Krakow = Location(street="", street_number="", city="Krakow", postcode="")
Bialystok = Location(street="", street_number="", city="Bialystok", postcode="")
Gdansk = Location(street="", street_number="", city="Gdansk", postcode="")
Lodz = Location(street="", street_number="", city="Lodz", postcode="")


USERS = [
    UserIn(email="courier@example.com", password="courier", role=UserRole.COURIER),
    UserIn(email="sender@example.com", password="sender", role=UserRole.SENDER),
    UserIn(email="admin@example.com", password="admin", role=UserRole.ADMIN),
]

SHIPMENTS = [
    ShipmentIn(
        origin=Warszawa,
        destination=Olsztyn,
        weight=100,
        recipient_email="example@example.com",
    ),
    ShipmentIn(
        origin=Olsztyn,
        destination=Lodz,
        weight=50,
        recipient_email="example@example.com",
    ),
    ShipmentIn(
        origin=Poznan,
        destination=Warszawa,
        weight=100,
        recipient_email="example@example.com",
    ),
    ShipmentIn(
        origin=Krakow,
        destination=Bialystok,
        weight=50,
        recipient_email="example@example.com",
    ),
    ShipmentIn(
        origin=Lodz,
        destination=Poznan,
        weight=56,
        recipient_email="example@example.com",
    ),
]
