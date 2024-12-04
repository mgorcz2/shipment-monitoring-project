
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict


class ShipmentDTO(BaseModel):
    id: int
    weight: float
    status: str
    origin_latitude: float
    origin_longitude: float

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls,record: Record) -> 'ShipmentDTO':
        record_dict=dict(record)

        return cls(
            id=record_dict.pop('id'),
            weight=record_dict.pop('weight'),
            status=record_dict.pop('status'),
            origin_latitude=record_dict.pop('origin_latitude'),
            origin_longitude=record_dict.pop('origin_longitude')
        )