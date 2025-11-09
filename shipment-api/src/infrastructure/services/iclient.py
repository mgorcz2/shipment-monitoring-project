"""Module containing client service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from uuid import UUID

from src.core.domain.user import ClientIn, UserIn
from src.infrastructure.dto.userDTO import ClientDTO


class IClientService(ABC):
    """An abstract class representing the protocol of client service."""

    @abstractmethod
    async def register_client_with_user(
        self, user_data: UserIn, client: ClientIn, user_id: UUID
    ) -> ClientDTO:
        """Register a new client.

        Args:
            client (ClientIn): The client input data to register.

        Returns:
            ClientDTO: The registered client object if successful.
        """

    @abstractmethod
    async def get_client(self, user_id: UUID) -> ClientDTO:
        """Get client by user_id.

        Args:
            user_id (UUID): UUID of the user.

        Returns:
            ClientDTO: The client object if exists.
        """

    @abstractmethod
    async def update_client(self, user_id: UUID, data: ClientIn) -> ClientDTO:
        """Update client by user_id.

        Args:
            user_id (UUID): The user id of the client.
            data (ClientIn): The updated client details.

        Returns:
            ClientDTO: The client object if updated.
        """

    @abstractmethod
    async def delete_client(self, user_id: UUID) -> ClientDTO:
        """Delete client by user_id.

        Args:
            user_id (UUID): The user id of the client.

        Returns:
            ClientDTO: The deleted client object.
        """

    @abstractmethod
    async def get_all_clients(self) -> Iterable[ClientDTO]:
        """Get all clients.

        Returns:
            Iterable[ClientDTO]: The client objects DTO details.
        """
