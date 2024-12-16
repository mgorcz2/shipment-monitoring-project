"""Module containing user repository abstractions."""


from abc import ABC, abstractmethod
from typing import Any, Iterable

from shipment_monitoring.core.domain.user import UserIn, User
from uuid import UUID

class IUserRepository(ABC):
    """An abstract repository class for user."""
    
    @abstractmethod
    async def register_user(self, user: UserIn) -> Any | None:
        """The abstract registering new user.

        Args:
            user (UserIn): The user input data.

        Returns:
            Any | None: The new user object if registered.
        """
    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> Any | None:
        """The abstract getting user by provided id.

        Args:
            user_id (UUID): UUID of the user.

        Returns:
            Any | None: The user object if exists._
        """
    @abstractmethod
    async def get_user_by_username(self, username: str) -> Any | None:
        """The abstract getting user by provided username.

        Args:
            username (str): The username of the user.

        Returns:
            Any | None: The user object if exists.
        """
        
    @abstractmethod
    async def detele_user(self, username: str) -> Any | None:
        """The abstract deleting user by provided username.

        Args:
            username (str): The username of the user.

        Returns:
            Any | None: The user object if deleted.
        """
        
    @abstractmethod
    async def update_user(self, username: str, data: User) -> Any | None:
        """The abstract updating user by provided username.

        Args:
            username (str): The username of the user.
            data (User): The updated user details.

        Returns:
            Any | None: The user object if updated.
        """