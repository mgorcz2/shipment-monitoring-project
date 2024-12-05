
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict
from shipment_monitoring.infrastructure.external.geopy import geopy
from shipment_monitoring.core.shared.ShipmentStatusEnum import ShipmentStatus

class ShipmentDTO(BaseModel):
    id: int
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
        
        origin = geopy.get_address(record_dict.pop('origin_latitude'), record_dict.pop('origin_longitude')) or "Unknown Address"
        destination = geopy.get_address(record_dict.pop('destination_latitude'), record_dict.pop('destination_longitude')) or "Uknown Address"
        return cls(
            id=record_dict.pop('id'),
            weight=record_dict.pop('weight'),
            status=record_dict.pop('status'),
            origin=origin,
            destination=destination
        )