"""Module containing user repository implementation."""

from typing import Any, Iterable

from sqlalchemy import select, delete, update

from shipment_monitoring.core.domain.user import UserIn, User
from shipment_monitoring.core.repositories.iuser import IUserRepository
from shipment_monitoring.db import (
    user_table, database
)
from shipment_monitoring.infrastructure.dto.userDTO import UserDTO
from uuid import UUID


class UserRepository(IUserRepository):
    """A class representing user DB repository."""
    
    async def register_user(self, data: UserIn) -> Any | None:
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

    async def get_user_by_id(self, user_id: UUID) -> Any | None:
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
        return user if user else None
    
    async def get_user_by_username(self,username) -> Any | None:
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
    
    async def detele_user(self, username: str) -> Any | None:
        """The abstract deleting user by provided username.

        Args:
            username (str): The username of the user.

        Returns:
            Any | None: The user object if deleted.
        """
        query = (
            delete(user_table)
            .where (user_table.c.username == username)
            .returning(user_table)
        )
        deleted_user = await database.fetch_one(query)
        return deleted_user if deleted_user else None
    
    async def update_user(self, username: str, data: User) -> Any | None:
        """The abstract updating user by provided username.

        Args:
            username (str): The username of the user.
            data (User): The updated user details.

        Returns:
            Any | None: The user object if updated.
        """
        query = (
            update(user_table)
            .where (user_table.c.username == username)
            .values(data.model_dump())
            .returning(user_table)
        )
        updated_user = await database.fetch_one(query)
        return updated_user if updated_user else None
    
    async def get_all_users(self) -> Iterable[Any] | None:
        """The method getting all users from database.

        Returns:
            Iterable[Any] | None: The user objects.
        """
        query = select(user_table)
        users = await database.fetch_all(query)
        return users