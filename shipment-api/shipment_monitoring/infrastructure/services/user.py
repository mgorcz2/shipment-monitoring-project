"""Module containing user service implementation."""

from typing import Iterable
from shipment_monitoring.core.domain.user import User, UserIn
from shipment_monitoring.infrastructure.dto.userDTO import UserDTO
from shipment_monitoring.infrastructure.services.iuser import IUserService
from shipment_monitoring.core.repositories.iuser import IUserRepository
from shipment_monitoring.core.security import consts
from shipment_monitoring.infrastructure.dto.tokenDTO import TokenDTO
from shipment_monitoring.core.security.token import create_access_token
from datetime import datetime, timedelta
from shipment_monitoring.core.security import password_hashing

from uuid import UUID


class UserService(IUserService):
    """A class representing implementation of user-related services."""

    _repository: IUserRepository

    def __init__(self, repository: IUserRepository):
        self._repository = repository

    async def register_user(self, user: UserIn) -> UserDTO | None:
        """The method for registering a new user in repository.

        Args:
            user (UserIn): The user input data.

        Returns:
            UserDTO | None: The user DTO details if exists.

        Raises:
            ValueError: If the username is already registered.
        """
        existing_user = await self._repository.get_user_by_username(user.username)
        if existing_user:
            raise ValueError("Username already registered")
        user.password = password_hashing.hash_password(user.password)
        return await self._repository.register_user(user)

    async def get_user_by_id(self, user_id: UUID) -> UserDTO | None:
        """The method getting user by provided id from repository.

        Args:
            user_id (UUID): UUID of the user.

        Returns:
            User | None: The user DTO details if exists.
        """
        user = await self._repository.get_user_by_id(user_id)
        return UserDTO.from_record(user) if user else None

    async def get_user_by_username(self, username) -> UserDTO | None:
        """The method getting user by provided username from repository.

        Args:
            username (str): The username of the user.

        Returns:
            User | None: The user object if exists.
        """
        user = await self._repository.get_user_by_username(username)
        return UserDTO.from_record(user) if user else None

    async def detele_user(self, username: str) -> dict | None:
        """The method deleting user by provided username.

        Args:
            username (str): The username of the user.

        Returns:
            User | None: The deleted user object from repository.
        """
        deleted_user = await self._repository.detele_user(username)
        return deleted_user if deleted_user else None

    async def update_user(self, username: str, data: User) -> dict | None:
        """The abstract updating user by provided username.

        Args:
            username (str): The username of the user.
            data (User): The updated user details.

        Returns:
            dict | None: The user object if updated.
        """
        existing_user = await self._repository.get_user_by_username(username)
        if not existing_user:
            raise ValueError("No user found with the provided username. Try again.")
        existing_user = await self._repository.get_user_by_username(data.username)
        if existing_user:
            raise ValueError("User with that username already registered.")
        existing_user = await self._repository.get_user_by_id(data.id)
        if existing_user:
            raise ValueError("User with that id already registered.")
        data.password = password_hashing.hash_password(data.password)
        updated_user = await self._repository.update_user(username, data)
        return updated_user if updated_user else None

    async def login_for_access_token(
        self, username: str, password: str
    ) -> TokenDTO | None:
        """The method for user authentication to get an access token.

        Args:
            username (str): The login identifier for the user
            password (str): The user's password for authentication.

        Returns:
            TokenDTO | None: A token DTO if login is successful, None otherwise.

        Raises:
            ValueError: If the users data is invalid.
        """

        user = await self._repository.get_user_by_username(username=username)
        if not user or not password_hashing.verify_password(password, user.password):
            raise ValueError("Incorrect username or password")
        access_token_expires = timedelta(minutes=consts.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    async def get_all_users(self) -> Iterable[UserDTO] | None:
        """The method getting all users from repository.

        Returns:
            Iterable[UserDTO] | None: The user objects DTO details.
        """
        users = await self._repository.get_all_users()
        return [UserDTO.from_record(user) for user in users]
