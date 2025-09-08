"""A model containing Location-related models."""

from pydantic import BaseModel


class Location(BaseModel):
    """Model representing Location attributes."""

    street: str = "Trebacka"
    street_number: str = "10"
    city: str = "Warszawa"
    postcode: str = "00-074"
