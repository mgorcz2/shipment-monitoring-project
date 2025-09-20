"""A model containing shipment-related models."""

import enum
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from src.core.domain.location import Location


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

    recipient_email: Optional[str] = ""
    recipient_id: Optional[UUID] = None
    origin: Location
    destination: Location


class Shipment(ShipmentIn):
    """The shipment model class"""

    id: int
    sender_id: UUID
    recipient_id: Optional[UUID] = None
    courier_id: Optional[UUID] = None
    status: ShipmentStatus
    origin_latitude: float
    origin_longitude: float
    destination_latitude: float
    destination_longitude: float
    created_at: datetime
    last_updated: datetime
    model_config = ConfigDict(from_attributes=True, extra="ignore")


class PackageIn(BaseModel):
    """An input package model"""

    weight: float
    length: float
    width: float
    height: float
    fragile: bool
    model_config = ConfigDict(from_attributes=True, extra="ignore")


class Package(PackageIn):
    """The package model class"""

    id: int
    created_at: datetime
    last_updated: datetime
    model_config = ConfigDict(from_attributes=True, extra="ignore")
