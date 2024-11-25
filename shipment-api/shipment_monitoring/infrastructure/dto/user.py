import string

from asyncpg import Record 
from pydantic import BaseModel, ConfigDict


class UserDTO(BaseModel):
    id: int
    username: string
    password: string
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
            password=record_dict.pop('password'),
            role=record_dict.pop('role')
        )