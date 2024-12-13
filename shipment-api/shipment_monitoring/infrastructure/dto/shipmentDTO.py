"""A module containing DTO models for output shipments."""
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict
from shipment_monitoring.core.domain.shipment import ShipmentStatus
from uuid import UUID
from typing import Optional


class ShipmentDTO(BaseModel):
    """A model representing DTO for shipment data."""
    id: int
    sender_id: UUID
    courier_id: Optional[UUID]
    weight: float
    recipient_email: Optional[str]
    
    status: ShipmentStatus
    origin : str
    destination: str
    
    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
        use_enum_values = True
    )

    @classmethod
    def from_record(cls,record: Record) -> 'ShipmentDTO':
        record_dict=dict(record)
        
        courier_id = record_dict.pop('courier_id', None)
        recipient_email = record_dict.pop('recipient_email', None)
        return cls(
            id=record_dict.pop('id'),
            sender_id=record_dict.pop('sender_id'),
            courier_id=courier_id,
            weight=record_dict.pop('weight'),
            recipient_email=recipient_email,
            status=record_dict.pop('status'),
            origin=record_dict.pop('origin'),
            destination=record_dict.pop('destination'),
            origin_coords=(
                            record_dict.pop('origin_latitude'),
                            record_dict.pop('origin_longitude')
                          ),
            destination_coords = (
                                    record_dict.pop('destination_latitude'),
                                    record_dict.pop('destination_longitude')
                                 )
        )
        
class ShipmentWithDistanceDTO(ShipmentDTO):
    """A model representing DTO for shipment with distance data."""
    origin_coords: tuple
    destination_coords: tuple
    origin_distance: float = -99999999
    destination_distance: float = -99999999
    