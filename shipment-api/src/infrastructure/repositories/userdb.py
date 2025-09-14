"""Module containing user repository implementation."""

from typing import Any, Iterable
from uuid import UUID

from sqlalchemy import delete, select, update

from src.core.domain.user import User, UserIn
from src.core.repositories.iuser import IUserRepository
from src.db import database, user_table


class UserRepository(IUserRepository):
    """A class representing user DB repository."""

    async def register_user(self, data: UserIn) -> User | None:
        """The method registering new user.

        Args:
            user (UserIn): The user input data.

        Returns:
            User | None: The user object if registered.
        """
        query = (
            user_table.insert()
            .values(email=data.email, password=data.password, role=data.role)
            .returning(user_table.c.id)
        )
        new_user_id = await database.execute(query)
        user_record = await self.get_user_by_id(new_user_id)
        return user_record if user_record else None

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        """The method getting user by provided id.

        Args:
            user_id (UUID): UUID of the user.

        Returns:
            UserDTO | None: The user DTO details if exists.
        """
        query = select(user_table).where(user_table.c.id == user_id)
        user = await database.fetch_one(query)
        return User(**user) if user else None

    async def get_user_by_email(self, email) -> User | None:
        """The method getting user by provided email.

        Args:
            email (str): The email of the user.

        Returns:
            User | None: The user object if exists.
        """

        query = select(user_table).where(user_table.c.email == email)
        user = await database.fetch_one(query)
        return User(**user) if user else None

    async def detele_user(self, email: str) -> User | None:
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
        return User(**deleted_user) if deleted_user else None

    async def update_user(self, email: str, data: UserIn) -> User | None:
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
        return User(**updated_user) if updated_user else None

    async def get_all_users(self) -> Iterable[User]:
        """The method getting all users from database.

        Returns:
            Iterable[Any]: The user objects.
        """
        query = select(user_table)
        users = await database.fetch_all(query)
        return [User(**user) for user in users]

    async def get_users_by_role(self, role) -> Iterable[User]:
        """The method getting user by provided role.

        Args:
            role (UserRole): Role of the users.

        Returns:
            Iterable[Any]: The user objects.
        """
        query = select(user_table).where(user_table.c.role == role)
        users = await database.fetch_all(query)
        return [User(**user) for user in users]
