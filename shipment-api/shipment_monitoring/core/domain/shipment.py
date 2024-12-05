from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from shipment_monitoring.core.domain.location import Location


class ShipmentIn(BaseModel): #ShipmentIn zawiera tylko te dane, które sa wymagane do stworzenia
    #courier_id: UUID
    #sender_id: UUID
    #created_at: datetime
    status: str
    
    origin: Location
    destination: Location

    weight: float

class Shipment(ShipmentIn):     #pelen obiekt
    id: int

    model_config = ConfigDict(from_attributes=True, extra='ignore')





