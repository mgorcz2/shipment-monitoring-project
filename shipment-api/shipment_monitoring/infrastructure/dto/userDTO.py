"""A module containing DTO models for output users."""

import string
from uuid import UUID

from asyncpg import Record
from pydantic import BaseModel, ConfigDict
from shipment_monitoring.core.domain.user import UserRole


class UserDTO(BaseModel):
    """A model representing DTO for user data."""

    id: UUID
    email: string
    role: UserRole

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
        use_enum_values=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "UserDTO":
        record_dict = dict(record)

        return cls(
            id=record_dict.pop("id"),
            email=record_dict.pop("email"),
            role=record_dict.pop("role"),
        )
