from pydantic import BaseModel, ConfigDict
from uuid import UUID
from shipment_monitoring.core.shared.UserRoleEnum import UserRole



class UserIn(BaseModel):
    username: str
    password: str
    role: UserRole = "admin"
    
class User(UserIn):
    id: UUID
    
    model_config = ConfigDict(from_attributes=True, extra='ignore')
