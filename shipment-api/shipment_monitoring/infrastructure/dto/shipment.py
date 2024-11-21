
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict


class ShipmentDTO(BaseModel):
    id: int
    origin: str
    destination: str
    weight: float
    status: str

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
            origin=record_dict.pop('origin'),
            destination=record_dict.pop('destination'),
            weight=record_dict.pop('weight'),
            status=record_dict.pop('status')
        )