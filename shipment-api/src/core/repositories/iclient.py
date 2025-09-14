"""Module containing client repository abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from uuid import UUID

from src.core.domain.user import ClientIn


class IClientRepository(ABC):
    """An abstract repository class for client."""

    @abstractmethod
    async def register_client(self, client: ClientIn, user_id: UUID) -> dict | None:
        """Register a new client and return joined client+user dict.

        Args:
            client (ClientIn): The client input data.
            user_id (UUID): The related user id.

        Returns:
            dict | None: The joined client+user dict if registered.
        """

    @abstractmethod
    async def get_client(self, client_id: UUID) -> dict | None:
        """Get client by provided client id (user_id), joined with user.

        Args:
            client_id (UUID): UUID of the client (user_id).

        Returns:
            dict | None: The joined client+user dict if exists.
        """

    @abstractmethod
    async def delete_client(self, client_id: UUID) -> dict | None:
        """Delete client by provided client id (user_id), joined with user.

        Args:
            client_id (UUID): UUID of the client (user_id).

        Returns:
            dict | None: The joined client+user dict if deleted.
        """

    @abstractmethod
    async def update_client(self, client_id: UUID, data: ClientIn) -> dict | None:
        """Update client by provided client id (user_id), joined with user.

        Args:
            client_id (UUID): UUID of the client (user_id).
            data (ClientIn): The updated client details.

        Returns:
            dict | None: The joined client+user dict if updated.
        """

    @abstractmethod
    async def get_all_clients(self) -> Iterable[dict] | None:
        """Get all clients, joined with user.

        Returns:
            Iterable[dict] | None: The joined client+user dicts.
        """
