"""Module containing user service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from uuid import UUID

from shipment_monitoring.core.domain.user import User, UserIn
from shipment_monitoring.infrastructure.dto.tokenDTO import TokenDTO
from shipment_monitoring.infrastructure.dto.userDTO import UserDTO


class IUserService(ABC):
    """An abstract class representing the protocol of user service."""

    @abstractmethod
    async def register_user(self, User: UserIn) -> UserDTO | None:
        """The abstract method for registering a new user in repository.

        Args:
            user (UserIn): The user input data to register.

        Returns:
            UserDTO | None: The registered user object if successful, None otherwise.
        """

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> UserDTO | None:
        """The abstract getting user by provided id from repository.

        Args:
            user_id (UUID): UUID of the user.

        Returns:
            UserDTO | None: The user object if exists.
        """

    @abstractmethod
    async def get_user_by_email(self, email) -> UserDTO | None:
        """The abstract getting user by provided email from repository.

        Args:
            email (str): The email of the user.

        Returns:
            User | None: The user object if exists.
        """

    @abstractmethod
    async def detele_user(self, email: str) -> dict | None:
        """The abstract deleting user by provided email.

        Args:
            email (str): The email of the user.

        Returns:
            dict | None: The deleted user object.
        """

    @abstractmethod
    async def update_user(self, email: str, data: User) -> dict | None:
        """The abstract updating user by provided email.

        Args:
            email (str): The email of the user.
            data (User): The updated user details.

        Returns:
            dict | None: The user object if updated.
        """

    @abstractmethod
    async def login_for_access_token(
        self, email: str, password: str
    ) -> TokenDTO | None:
        """The abstract method for user authentication to get an access token.

        Args:
            email (str): The login identifier for the user
            password (str): The user's password for authentication.

        Returns:
            TokenDTO | None: A token DTO if login is successful, None otherwise.
        """

    async def get_all_users(self) -> Iterable[UserDTO] | None:
        """The abstract getting all users.

        Returns:
            Iterable[UserDTO] | None: The user objects DTO details.
        """
