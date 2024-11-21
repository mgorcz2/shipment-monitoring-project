from typing import Any, Iterable

from sqlalchemy import select

from shipment_monitoring.core.domain.user import UserIn, User
from shipment_monitoring.core.repositories.iuser import IUserRepository
from shipment_monitoring.db import (
    user_table, database
)
from shipment_monitoring.infrastructure.dto.user import UserDTO


class UserRepository(IUserRepository):
    async def add_user(self, data: UserIn) -> Any | None:
        query = user_table.insert().values(**data.model_dump())
        new_user = await database.execute(query)
        new_user = await self.get_user_by_id(new_user)
        return User(**dict(new_user)) if new_user else None

    async def get_user_by_id(self, user_id: Any) -> Any | None:
        query = (
            select(user_table)
            .where(user_table.c.id == user_id)
        )
        user = await database.fetch_one(query)
        return UserDTO.from_record(user) if user else None
