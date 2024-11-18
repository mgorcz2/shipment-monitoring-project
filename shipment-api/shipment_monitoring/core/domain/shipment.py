from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ShipmentIn(BaseModel): #ShipmentIn zawiera tylko te dane, które sa wymagane do stworzenia
    origin: str
    destination: str
    weight: float
    status: str

class Shipment(ShipmentIn):     #pelen obiekt
    id: int

    model_config = ConfigDict(from_attributes=True, extra='ignore')