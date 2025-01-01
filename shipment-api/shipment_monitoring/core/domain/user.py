"""A model containing user-related models."""


from pydantic import BaseModel, ConfigDict
from uuid import UUID
import enum

class UserRole(str, enum.Enum):
    """The user role enum class."""
    COURIER = "courier"
    SENDER = "sender"
    ADMIN = "admin"


class UserIn(BaseModel):
    """An input user model"""
    username: str
    password: str
    role: UserRole = "admin"
    

class User(UserIn):
    """The user model class"""
    id: UUID
    model_config = ConfigDict(from_attributes=True, extra='ignore')
