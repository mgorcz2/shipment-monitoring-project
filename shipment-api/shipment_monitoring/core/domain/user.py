"""A model containing user-related models."""

import enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserRole(str, enum.Enum):
    """The user role enum class."""

    COURIER = "courier"
    SENDER = "sender"
    ADMIN = "admin"


class UserIn(BaseModel):
    """An input user model"""

    email: EmailStr
    password: str
    role: UserRole = "sender"


class User(UserIn):
    """The user model class"""

    id: UUID
    model_config = ConfigDict(from_attributes=True, extra="ignore")
