from abc import ABC, abstractmethod
from typing import Any, Iterable

from shipment_monitoring.core.domain.user import UserIn
from uuid import UUID

class IUserRepository(ABC):

    @abstractmethod
    async def register_user(self, user: UserIn) -> Any | None:
        pass
    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> Any | None:
        pass
    @abstractmethod
    async def get_user_by_username(self,username) -> Any | None:
        pass
 