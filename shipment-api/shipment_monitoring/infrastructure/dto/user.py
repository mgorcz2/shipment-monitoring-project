import string

from asyncpg import Record 
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class UserDTO(BaseModel):
    id: UUID
    username: string
    role: string
        
    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> 'UserDTO':
        record_dict = dict(record)

        return cls(
            id=record_dict.pop('id'),
            username=record_dict.pop('username'),
            role=record_dict.pop('role')
        )