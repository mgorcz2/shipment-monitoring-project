from abc import ABC, abstractmethod
from typing import Any, Iterable

from shipment_monitoring.core.domain.user import UserIn


class IUserRepository(ABC):

    @abstractmethod
    async def register_user(self, user: UserIn) -> None:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: Any) -> Any | None:
        pass
    @abstractmethod
    async def get_user_by_username(self,username) -> Any | None:
        pass
    
    @abstractmethod
    async def login_user(self, username, password) -> Any | None:
        pass