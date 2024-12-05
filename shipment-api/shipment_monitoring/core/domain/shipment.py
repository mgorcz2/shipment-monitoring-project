from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from shipment_monitoring.core.domain.location import Location
from shipment_monitoring.core.shared.ShipmentStatusEnum import ShipmentStatus


class ShipmentIn(BaseModel): #ShipmentIn zawiera tylko te dane, które sa wymagane do stworzenia
    #courier_id: UUID
    #sender_id: UUID
    #created_at: datetime
    #status: ShipmentStatus = "ready_for_pickup"
    origin: Location
    destination: Location

    weight: float

class Shipment(ShipmentIn):     #pelen obiekt
    id: int
    status: ShipmentStatus
    model_config = ConfigDict(from_attributes=True, extra='ignore')





