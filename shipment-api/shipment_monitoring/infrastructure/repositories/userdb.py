from typing import Any, Iterable

from sqlalchemy import select

from shipment_monitoring.api.security import utils
from shipment_monitoring.core.domain.user import UserIn, User
from shipment_monitoring.core.repositories.iuser import IUserRepository
from shipment_monitoring.db import (
    user_table, database
)
from shipment_monitoring.infrastructure.dto.user import UserDTO



class UserRepository(IUserRepository):
    
    async def register_user(self, data: UserIn) -> Any | None:
        query = user_table.insert().values(username=data.username,password=data.password, role=data.role)
        new_user = await database.execute(query)
        new_user = await self.get_user_by_id(new_user)
        return UserDTO.from_record(new_user) if new_user else None

    async def get_user_by_id(self, user_id: Any) -> UserDTO | None:
        query = (
            select(user_table)
            .where(user_table.c.id == user_id)
        )
        user = await database.fetch_one(query)
        return UserDTO.from_record(user) if user else None
    
    async def get_user_by_username(self,username) -> Any | None:
        query = (
            select (user_table)
            .where (user_table.c.username == username)
        )
        user = await database.fetch_one(query)
        return UserDTO.from_record(user) if user else None

