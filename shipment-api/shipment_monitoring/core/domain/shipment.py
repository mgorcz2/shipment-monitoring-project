from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ShipmentIn(BaseModel):
    origin: str
    destination: str
    weight: float
    status: str

class Shipment(ShipmentIn):
    id: int

    model_config = ConfigDict(from_attributes=True, extra='ignore')