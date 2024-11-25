from abc import ABC, abstractmethod
from typing import Iterable
from shipment_monitoring.core.domain.user import User,UserIn

class IUserService(ABC):
    @abstractmethod
    async def register_user(self,User: UserIn) -> User | None:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id) -> User | None:
        pass
    
    @abstractmethod
    async def get_user_by_username(self,username) -> User | None:
        pass
    
