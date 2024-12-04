from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class ShipmentIn(BaseModel): #ShipmentIn zawiera tylko te dane, które sa wymagane do stworzenia
    #courier_id: UUID
    #sender_id: UUID
    #created_at: datetime
    status: str
    
    
    origin_street: str
    origin_street_number: str
    origin_city: str
    origin_postcode: str
    destination_street: str
    destination_street_number: str
    destination_city: str
    destination_postcode: str

    weight: float

class Shipment(ShipmentIn):     #pelen obiekt
    id: int

    model_config = ConfigDict(from_attributes=True, extra='ignore')





