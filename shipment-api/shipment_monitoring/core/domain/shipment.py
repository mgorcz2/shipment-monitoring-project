"""A model containing shipment-related models."""

from typing import Optional
from datetime import datetime
import enum
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from shipment_monitoring.core.domain.location import Location


class ShipmentStatus(str, enum.Enum):
    """The shipment status enum class."""

    READY_FOR_PICKUP = "ready_for_pickup"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    FAILED_ATTEMPT = "failed_attempt"
    RETURNED_TO_SENDER = "returned_to_sender"
    LOST = "lost"
    DAMAGED = "damaged"


class ShipmentIn(BaseModel):
    """An input shipment model"""

    origin: Location
    destination: Location
    weight: float
    recipient_email: Optional[str] = ""


class Shipment(ShipmentIn):
    """The shipment model class"""

    id: int
    sender_id: UUID
    courier_id: Optional[UUID] = None
    status: ShipmentStatus
    created_at: datetime
    last_updated: datetime
    model_config = ConfigDict(from_attributes=True, extra="ignore")
