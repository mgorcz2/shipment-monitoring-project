import string

from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict


class UserDTO(BaseModel):
    id: int
    login: string
    password: string

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
            login=record_dict.pop('login'),
            password=record_dict.pop('password'),
        )