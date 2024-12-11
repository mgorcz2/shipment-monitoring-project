"""Module containing user repository implementation."""

from typing import Any, Iterable

from sqlalchemy import select

from shipment_monitoring.core.domain.user import UserIn, User
from shipment_monitoring.core.repositories.iuser import IUserRepository
from shipment_monitoring.db import (
    user_table, database
)
from shipment_monitoring.infrastructure.dto.userDTO import UserDTO
from uuid import UUID


class UserRepository(IUserRepository):
    """A class representing user DB repository."""
    
    async def register_user(self, data: UserIn) -> UserDTO | None:
        """The method registering new user.

        Args:
            user (UserIn): The user input data.

        Returns:
            UserDTO | None: The user DTO details if exists.
        """
        query = user_table.insert().values(username=data.username,password=data.password, role=data.role)
        new_user = await database.execute(query)
        new_user = await self.get_user_by_id(new_user)
        return UserDTO.from_record(new_user) if new_user else None

    async def get_user_by_id(self, user_id: UUID) -> UserDTO | None:
        """The method getting user by provided id.

        Args:
            user_id (UUID): UUID of the user.

        Returns:
            UserDTO | None: The user DTO details if exists.
        """
        query = (
            select(user_table)
            .where(user_table.c.id == user_id)
        )
        user = await database.fetch_one(query)
        return UserDTO.from_record(user) if user else None
    
    async def get_user_by_username(self,username) -> User | None:
        """The method getting user by provided username.

        Args:
            username (str): The username of the user.

        Returns:
            User | None: The user object if exists.
        """
 
        query = (
            select (user_table)
            .where (user_table.c.username == username)
        )
        user = await database.fetch_one(query)
        return user if user else None

