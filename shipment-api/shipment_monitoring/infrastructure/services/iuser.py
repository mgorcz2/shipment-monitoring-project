"""Module containing user service abstractions."""

from abc import ABC, abstractmethod
from shipment_monitoring.core.domain.user import User,UserIn
from shipment_monitoring.infrastructure.dto.tokenDTO import TokenDTO
from uuid import UUID
class IUserService(ABC):
    """An abstract class representing the protocol of user service."""
    
    @abstractmethod
    async def register_user(self,User: UserIn) -> User | None:
        """The abstract method for registering a new user in repository.

        Args:
            user (UserIn): The user input data to register.

        Returns:
            User | None: The registered user object if successful, None otherwise.
        """

    @abstractmethod
    async def get_user_by_id(self, user_id:UUID) -> User | None:
        """The abstract getting user by provided id from repository.

        Args:
            user_id (UUID): UUID of the user.

        Returns:
            User | None: The user object if exists.
        """
    
    @abstractmethod
    async def get_user_by_username(self,username) -> User | None:
        """The abstract getting user by provided username from repository.

        Args:
            username (str): The username of the user.

        Returns:
            User | None: The user object if exists.
        """
    
    @abstractmethod
    async def login_for_access_token(self, username: str, password: str) -> TokenDTO | None:
        """The abstract method for user authentication to get an access token.

        Args:
            username (str): The login identifier for the user
            password (str): The user's password for authentication.

        Returns:
            TokenDTO | None: A token DTO if login is successful, None otherwise.
        """
    
