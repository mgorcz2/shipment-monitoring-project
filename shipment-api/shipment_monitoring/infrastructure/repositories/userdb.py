from typing import Any, Iterable

from sqlalchemy import select

from shipment_monitoring.core.domain.user import UserIn, User
from shipment_monitoring.core.repositories.iuser import IUserRepository
from shipment_monitoring.db import (
    user_table, database
)
from shipment_monitoring.infrastructure.dto.user import UserDTO
from passlib.context import CryptContext



pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
async def hash_password(password) -> str:
    return pwd_context.hash(password)


class UserRepository(IUserRepository):

    async def register_user(self, data: UserIn) -> Any | None:
        exist = await self.get_user_by_username(data.username)
        if exist:
            return None
        hashed_password = await hash_password(data.password)
        query = user_table.insert().values(username=data.username,password=hashed_password)
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

    async def login_user(self,username,password) -> Any | None:
        query = (
            select (user_table)
            .where(user_table.c.username == username)
        )
        user = await database.fetch_one(query)
        if user:
            if pwd_context.verify(password, user.password):
                return UserDTO.from_record(user) if user else None


