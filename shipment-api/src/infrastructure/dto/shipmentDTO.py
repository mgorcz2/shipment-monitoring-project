"""A module containing DTO models for output shipments."""

from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict
from shipment_monitoring.core.domain.shipment import ShipmentStatus
from uuid import UUID
from typing import Optional
from datetime import datetime


class ShipmentDTO(BaseModel):
    """A model representing DTO for shipment data."""

    id: int
    sender_id: UUID
    courier_id: Optional[UUID]
    weight: float
    recipient_email: Optional[str]
    status: ShipmentStatus
    origin: str
    destination: str
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

        courier_id = record_dict.pop("courier_id", None)
        recipient_email = record_dict.pop("recipient_email", None)
        return cls(
            id=record_dict.pop("id"),
            sender_id=record_dict.pop("sender_id"),
            courier_id=courier_id,
            weight=record_dict.pop("weight"),
            recipient_email=recipient_email,
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
            created_at=record_dict.pop("created_at"),
            last_updated=record_dict.pop("last_updated"),
        )


class ShipmentWithDistanceDTO(ShipmentDTO):
    """A model representing DTO for shipment with distance data."""

    origin_coords: tuple
    destination_coords: tuple
    origin_distance: Optional[float] = None
    destination_distance: Optional[float] = None
