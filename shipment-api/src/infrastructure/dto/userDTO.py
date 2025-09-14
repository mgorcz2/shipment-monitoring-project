"""A module containing DTO models for output users."""

from uuid import UUID

from asyncpg import Record
from pydantic import BaseModel, ConfigDict

from src.core.domain.user import UserRole


class UserDTO(BaseModel):
    """A model representing DTO for user data."""

    id: UUID
    email: str
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


class StaffDTO(BaseModel):
    """A model representing DTO for staff user data."""

    id: UUID
    email: str
    role: UserRole
    first_name: str
    last_name: str
    phone_number: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
        use_enum_values=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "StaffDTO":
        record_dict = dict(record)

        return cls(
            id=record_dict.pop("id"),
            email=record_dict.pop("email"),
            role=record_dict.pop("role"),
            first_name=record_dict.pop("first_name"),
            last_name=record_dict.pop("last_name"),
            phone_number=record_dict.pop("phone_number"),
        )


class ClientDTO(BaseModel):
    """A model representing DTO for client user data."""

    id: UUID
    email: str
    role: UserRole
    first_name: str
    last_name: str
    phone_number: str
    address: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
        use_enum_values=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "ClientDTO":
        record_dict = dict(record)
        return cls(
            id=record_dict.pop("id"),
            email=record_dict.pop("email"),
            role=record_dict.pop("role"),
            first_name=record_dict.pop("first_name"),
            last_name=record_dict.pop("last_name"),
            phone_number=record_dict.pop("phone_number"),
            address=record_dict.pop("address", None),
        )
