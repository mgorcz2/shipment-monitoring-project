"""A model containing user-related models."""

import enum
import re
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, constr, field_validator


class UserRole(str, enum.Enum):
    """The user role enum class."""

    MANAGER = "manager"
    COURIER = "courier"
    SENDER = "sender"
    ADMIN = "admin"


class UserIn(BaseModel):
    """An input user model"""

    email: EmailStr = Field(..., description="The email of the user")
    password: str = Field(
        ...,
        description="The password of the user",
        min_length=8,
        max_length=128,
    )
    role: UserRole = "sender"

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[0-9\W]", value):
            raise ValueError(
                "Password must contain at least one number or special character"
            )
        return value


class User(UserIn):
    """The user model class"""

    id: UUID
    model_config = ConfigDict(from_attributes=True, extra="ignore")


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=8, max_length=128)] = None
    role: Optional[UserRole] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, value) -> Optional[str]:
        return UserIn.validate_password(value)
