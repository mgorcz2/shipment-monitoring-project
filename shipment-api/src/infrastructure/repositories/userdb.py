"""Module containing user repository implementation."""

from typing import Any, Iterable
from uuid import UUID

from sqlalchemy import delete, select, update

from shipment_monitoring.core.domain.user import UserIn
from shipment_monitoring.core.repositories.iuser import IUserRepository
from shipment_monitoring.db import database, user_table


class UserRepository(IUserRepository):
    """A class representing user DB repository."""

    async def register_user(self, data: UserIn) -> Any | None:
        """The method registering new user.

        Args:
            user (UserIn): The user input data.

        Returns:
            UserDTO | None: The user DTO details if exists.
        """
        query = user_table.insert().values(
            email=data.email, password=data.password, role=data.role
        )
        new_user = await database.execute(query)
        new_user = await self.get_user_by_id(new_user)
        return new_user if new_user else None

    async def get_user_by_id(self, user_id: UUID) -> Any | None:
        """The method getting user by provided id.

        Args:
            user_id (UUID): UUID of the user.

        Returns:
            UserDTO | None: The user DTO details if exists.
        """
        query = select(user_table).where(user_table.c.id == user_id)
        user = await database.fetch_one(query)
        return user if user else None

    async def get_user_by_email(self, email) -> Any | None:
        """The method getting user by provided email.

        Args:
            email (str): The email of the user.

        Returns:
            User | None: The user object if exists.
        """

        query = select(user_table).where(user_table.c.email == email)
        user = await database.fetch_one(query)
        return user if user else None

    async def detele_user(self, email: str) -> Any | None:
        """The abstract deleting user by provided email.

        Args:
            email (str): The email of the user.

        Returns:
            Any | None: The user object if deleted.
        """
        query = (
            delete(user_table).where(user_table.c.email == email).returning(user_table)
        )
        deleted_user = await database.fetch_one(query)
        return deleted_user if deleted_user else None

    async def update_user(self, email: str, data: UserIn) -> Any | None:
        """The abstract updating user by provided email.

        Args:
            email (str): The email of the user.
            data (User): The updated user details.

        Returns:
            Any | None: The user object if updated.
        """
        query = (
            update(user_table)
            .where(user_table.c.email == email)
            .values(data.model_dump())
            .returning(user_table)
        )
        updated_user = await database.fetch_one(query)
        return updated_user if updated_user else None

    async def get_all_users(self) -> Iterable[Any]:
        """The method getting all users from database.

        Returns:
            Iterable[Any]: The user objects.
        """
        query = select(user_table)
        users = await database.fetch_all(query)
        return users

    async def get_users_by_role(self, role) -> Iterable[Any]:
        """The method getting user by provided role.

        Args:
            role (UserRole): Role of the users.

        Returns:
            Iterable[Any]: The user objects.
        """
        query = select(user_table).where(user_table.c.role == role)
        users = await database.fetch_all(query)
        return users
