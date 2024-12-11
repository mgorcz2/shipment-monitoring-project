
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict
from shipment_monitoring.infrastructure.external.geopy import geopy
from shipment_monitoring.core.shared.ShipmentStatusEnum import ShipmentStatus
from uuid import UUID


class ShipmentDTO(BaseModel):
    id: int
    sender_id: UUID
    weight: float
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
        
        return cls(
            id=record_dict.pop('id'),
            sender_id=record_dict.pop('sender_id'),
            weight=record_dict.pop('weight'),
            status=record_dict.pop('status'),
            origin=record_dict.pop('origin'),
            destination=record_dict.pop('destination'),
            origin_latitude=record_dict.pop('origin_latitude'),
            origin_longitude = record_dict.pop('origin_longitude'),
            destination_latitude = record_dict.pop('destination_latitude'),
            destination_longitude = record_dict.pop('destination_longitude')
        )
        
class ShipmentWithDistanceDTO(ShipmentDTO):
    origin_latitude: float
    origin_longitude: float
    destination_latitude: float
    destination_longitude: float
    origin_distance: float = -99999999
    destination_distance: float = -99999999
    