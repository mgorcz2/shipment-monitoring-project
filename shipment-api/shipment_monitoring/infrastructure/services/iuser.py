from abc import ABC, abstractmethod
from shipment_monitoring.core.domain.user import User,UserIn
from shipment_monitoring.api.utils.token import TokenDTO
from uuid import UUID
class IUserService(ABC):
    @abstractmethod
    async def register_user(self,User: UserIn) -> User | None:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id:UUID) -> User | None:
        pass
    
    @abstractmethod
    async def get_user_by_username(self,username) -> User | None:
        pass
    
    @abstractmethod
    async def login_for_access_token(self, login, password) -> TokenDTO | None:
        pass
    
