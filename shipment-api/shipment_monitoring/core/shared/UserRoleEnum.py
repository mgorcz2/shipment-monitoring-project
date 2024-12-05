import enum
class UserRole(str, enum.Enum):
    COURIER = "courier"
    SENDER = "sender"
    ADMIN = "admin"
