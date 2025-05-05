"""Module containing user service implementation."""

from datetime import datetime, timedelta
from typing import Iterable
from uuid import UUID

from shipment_monitoring.core.domain.user import User, UserIn, UserUpdate
from shipment_monitoring.core.repositories.iuser import IUserRepository
from shipment_monitoring.core.security import consts, password_hashing
from shipment_monitoring.core.security.token import create_access_token
from shipment_monitoring.infrastructure.dto.tokenDTO import TokenDTO
from shipment_monitoring.infrastructure.dto.userDTO import UserDTO
from shipment_monitoring.infrastructure.services.iuser import IUserService


class UserService(IUserService):
    """A class representing implementation of user-related services."""

    _repository: IUserRepository

    def __init__(self, repository: IUserRepository):
        self._repository = repository

    async def register_user(self, user: UserIn) -> UserDTO:
        """The method for registering a new user in repository.

        Args:
            user (UserIn): The user input data.

        Returns:
            UserDTO: The user DTO details if exists.

        Raises:
            ValueError: If the email is already registered.
        """
        existing_user = await self._repository.get_user_by_email(user.email)
        if existing_user:
            raise ValueError("User with that email already registered.")
        user.password = password_hashing.hash_password(user.password)
        user = await self._repository.register_user(user)
        if not user:
            raise ValueError("Failed to register the user. Please try again.")
        return UserDTO.from_record(user) if user else None

    async def get_user_by_id(self, user_id: UUID) -> UserDTO:
        """The method getting user by provided id from repository.

        Args:
            user_id (UUID): UUID of the user.

        Returns:
            User: The user DTO details if exists.
        """
        user = await self._repository.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"No user found with the provided ID: {user_id}")
        return UserDTO.from_record(user)

    async def get_user_by_email(self, email) -> UserDTO:
        """The method getting user by provided email from repository.

        Args:
            email (str): The email of the user.

        Returns:
            User: The user object if exists.
        """
        user = await self._repository.get_user_by_email(email)
        if not user:
            raise ValueError(f"No user found with the provided email: {email}")
        return UserDTO.from_record(user)

    async def detele_user(self, email: str) -> User:
        """The method deleting user by provided email.

        Args:
            email (str): The email of the user.

        Returns:
            User: The deleted user object from repository.
        """
        deleted_user = await self._repository.detele_user(email)
        if not deleted_user:
            raise ValueError(f"No user found with the provided email: {email}")
        return deleted_user

    async def update_user(self, email: str, update_data: UserUpdate) -> User:
        """The abstract updating user by provided email.

        Args:
            email (str): The email of the user.
            data (UserUpdate): The updated user details.

        Returns:
            User: The user object if updated.
        """
        original_user = await self._repository.get_user_by_email(email)
        if not original_user:
            raise ValueError("No user found with the provided email. Try again.")
        if update_data.email and update_data.email != email:
            user_with_new_email = await self._repository.get_user_by_email(
                update_data.email
            )
            if user_with_new_email:
                raise ValueError("User with that email already registered.")
        updated_user = UserIn(
            email=update_data.email if update_data.email else original_user["email"],
            password=(
                update_data.password
                if update_data.password
                else original_user["password"]
            ),
            role=update_data.role if update_data.role else original_user["role"],
        )
        updated_user.password = password_hashing.hash_password(update_data.password)
        updated_user = await self._repository.update_user(email, updated_user)
        if not updated_user:
            raise ValueError("Failed to update the user. Please try again.")
        return updated_user

    async def login_for_access_token(self, email: str, password: str) -> TokenDTO:
        """The method for user authentication to get an access token.

        Args:
            email (str): The login identifier for the user
            password (str): The user's password for authentication.

        Returns:
            TokenDTO: A token DTO if login is successful, None otherwise.

        Raises:
            ValueError: If the users data is invalid.
        """

        user = await self._repository.get_user_by_email(email=email)
        if not user or not password_hashing.verify_password(password, user.password):
            raise ValueError("Incorrect email or password")
        access_token = create_access_token(data={"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer"}

    async def get_all_users(self) -> Iterable[UserDTO]:
        """The method getting all users from repository.

        Returns:
            Iterable[UserDTO]: The user objects DTO details.
        """
        users = await self._repository.get_all_users()
        if not users:
            raise ValueError("No users found in the repository.")
        return [UserDTO.from_record(user) for user in users]

    async def get_users_by_role(self, role) -> Iterable[UserDTO]:
        """The method getting user by provided role.

        Args:
            role (UserRole): Role of the users.

        Returns:
            Iterable[UserDTO]: The user objects DTO details.
        """
        users = await self._repository.get_users_by_role(role)
        if not users:
            raise ValueError(f"No users found with the role: {role}")
        return [UserDTO.from_record(user) for user in users]
