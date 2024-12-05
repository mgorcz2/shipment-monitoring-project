from pydantic import BaseModel

class Location(BaseModel):
    street: str = "Trebacka"
    street_number: str = "10"
    city: str = "Warszawa"
    postcode: str ="00-074"