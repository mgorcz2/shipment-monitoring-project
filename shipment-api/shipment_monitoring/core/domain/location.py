from pydantic import BaseModel

class Location(BaseModel):
    street: str
    street_number: str
    city: str
    postcode: str