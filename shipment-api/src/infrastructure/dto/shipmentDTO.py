"""A module containing DTO models for output shipments."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict

from src.core.domain.shipment import ShipmentStatus


class ShipmentDTO(BaseModel):
    """A model representing DTO for shipment data."""

    id: int
    sender_id: Optional[UUID]
    recipient_id: Optional[UUID]
    courier_id: Optional[UUID]
    sender_fullname: Optional[str]
    recipient_fullname: Optional[str]
    recipient_email: Optional[str]
    status: ShipmentStatus
    origin: str
    destination: str
    origin_coords: tuple
    destination_coords: tuple
    origin_distance: Optional[float] = None
    destination_distance: Optional[float] = None
    created_at: datetime
    last_updated: datetime

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
        use_enum_values=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "ShipmentDTO":
        record_dict = dict(record)

        return cls(
            id=record_dict.pop("id"),
            courier_id=record_dict.pop("courier_id", None),
            recipient_id=record_dict.pop("recipient_id", None),
            sender_fullname=record_dict.pop("sender_fullname", None),
            recipient_fullname=record_dict.pop("recipient_fullname", None),
            recipient_email=record_dict.pop("recipient_email", None),
            sender_id=record_dict.pop("sender_id", None),
            status=record_dict.pop("status"),
            origin=record_dict.pop("origin"),
            destination=record_dict.pop("destination"),
            origin_coords=(
                record_dict.pop("origin_latitude"),
                record_dict.pop("origin_longitude"),
            ),
            destination_coords=(
                record_dict.pop("destination_latitude"),
                record_dict.pop("destination_longitude"),
            ),
            origin_distance=record_dict.pop("origin_distance", None),
            destination_distance=record_dict.pop("destination_distance", None),
            created_at=record_dict.pop("created_at"),
            last_updated=record_dict.pop("last_updated"),
        )


class ShipmentWithDistanceDTO(ShipmentDTO):
    """A model representing DTO for shipment with distance data."""

    origin_coords: tuple
    destination_coords: tuple
    origin_distance: Optional[float] = None
    destination_distance: Optional[float] = None


class PackageDTO(BaseModel):
    """A model representing DTO for package data."""

    id: int
    weight: float
    length: float
    width: float
    height: float
    fragile: bool
    created_at: datetime
    last_updated: datetime
    pickup_scheduled_date: Optional[datetime]
    pickup_actual_date: Optional[datetime]
    delivery_scheduled_date: Optional[datetime]
    delivery_actual_date: Optional[datetime]
    cancelled_at: Optional[datetime]
    note: Optional[str]

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "PackageDTO":
        record_dict = dict(record)

        return cls(
            id=record_dict.pop("id"),
            weight=record_dict.pop("weight"),
            length=record_dict.pop("length"),
            width=record_dict.pop("width"),
            height=record_dict.pop("height"),
            fragile=record_dict.pop("fragile"),
            created_at=record_dict.pop("created_at"),
            last_updated=record_dict.pop("last_updated"),
            pickup_scheduled_date=record_dict.pop("pickup_scheduled_date"),
            pickup_actual_date=record_dict.pop("pickup_actual_date"),
            delivery_scheduled_date=record_dict.pop("delivery_scheduled_date"),
            delivery_actual_date=record_dict.pop("delivery_actual_date"),
            cancelled_at=record_dict.pop("cancelled_at"),
            note=record_dict.pop("note", None),
        )
