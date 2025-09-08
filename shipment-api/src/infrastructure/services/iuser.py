"""Module containing user service abstractions."""

# pylint: disable=redefined-outer-name
from abc import ABC, abstractmethod
from typing import Iterable
from uuid import UUID

from shipment_monitoring.core.domain.user import User, UserIn, UserUpdate
from shipment_monitoring.infrastructure.dto.tokenDTO import TokenDTO
from shipment_monitoring.infrastructure.dto.userDTO import UserDTO


class IUserService(ABC):
    """An abstract class representing the protocol of user service."""

    @abstractmethod
    async def register_user(self, user: UserIn) -> UserDTO:
        """The abstract method for registering a new user in repository.

        Args:
            user (UserIn): The user input data to register.

        Returns:
            UserDTO: The registered user object if successful, None otherwise.
        """

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> UserDTO:
        """The abstract getting user by provided id from repository.

        Args:
            user_id (UUID): UUID of the user.

        Returns:
            UserDTO: The user object if exists.
        """

    @abstractmethod
    async def get_user_by_email(self, email) -> UserDTO:
        """The abstract getting user by provided email from repository.

        Args:
            email (str): The email of the user.

        Returns:
            User: The user object if exists.
        """

    @abstractmethod
    async def detele_user(self, email: str) -> User:
        """The abstract deleting user by provided email.

        Args:
            email (str): The email of the user.

        Returns:
            User: The deleted user object.
        """

    @abstractmethod
    async def update_user(self, email: str, data: UserUpdate) -> User:
        """The abstract updating user by provided email.

        Args:
            email (str): The email of the user.
            data (UserUpdate): The updated user details.

        Returns:
            User: The user object if updated.
        """

    @abstractmethod
    async def login_for_access_token(self, email: str, password: str) -> TokenDTO:
        """The abstract method for user authentication to get an access token.

        Args:
            email (str): The login identifier for the user
            password (str): The user's password for authentication.

        Returns:
            TokenDTO: A token DTO if login is successful, None otherwise.
        """

    @abstractmethod
    async def get_all_users(self) -> Iterable[UserDTO]:
        """The abstract getting all users.

        Returns:
            Iterable[UserDTO]: The user objects DTO details.
        """

    @abstractmethod
    async def get_users_by_role(self, role) -> Iterable[UserDTO]:
        """The method getting user by provided role.

        Args:
            role (UserRole): Role of the users.

        Returns:
            Iterable[UserDTO]: The user objects DTO details.
        """
