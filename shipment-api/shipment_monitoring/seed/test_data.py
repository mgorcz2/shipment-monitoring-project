"""Data for testing"""

from shipment_monitoring.core.domain.user import UserRole, UserIn
from shipment_monitoring.core.domain.shipment import ShipmentStatus, ShipmentIn
from shipment_monitoring.core.domain.location import Location

Warszawa = Location(street="", street_number="", city="Warszawa", postcode="")
Olsztyn = Location(street="", street_number="", city="Olsztyn", postcode="")
Poznan = Location(street="", street_number="", city="Poznan", postcode="")
Krakow = Location(street="", street_number="", city="Krakow", postcode="")
Bialystok = Location(street="", street_number="", city="Bialystok", postcode="")
Gdansk = Location(street="", street_number="", city="Gdansk", postcode="")
Lodz = Location(street="", street_number="", city="Lodz", postcode="")


USERS = [
    UserIn(username="courier", password="courier", role=UserRole.COURIER),
    UserIn(username="sender", password="sender", role=UserRole.SENDER),
]

SHIPMENTS = [
    ShipmentIn(
        origin=Warszawa,
        destination=Olsztyn,
        weight=100,
        recipient_email="example@gmail.com",
    ),
    ShipmentIn(
        origin=Olsztyn, destination=Lodz, weight=50, recipient_email="example@gmail.com"
    ),
    ShipmentIn(
        origin=Poznan,
        destination=Warszawa,
        weight=100,
        recipient_email="example@gmail.com",
    ),
    ShipmentIn(
        origin=Krakow,
        destination=Bialystok,
        weight=50,
        recipient_email="example@gmail.com",
    ),
    ShipmentIn(
        origin=Lodz, destination=Poznan, weight=56, recipient_email="example@gmail.com"
    ),
]
