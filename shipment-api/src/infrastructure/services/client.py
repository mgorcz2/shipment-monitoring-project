"""Module containing client service implementation."""

from typing import Iterable
from uuid import UUID

from src.core.domain.user import ClientIn
from src.core.repositories.iclient import IClientRepository
from src.infrastructure.dto.userDTO import ClientDTO
from src.infrastructure.services.iclient import IClientService


class ClientService(IClientService):
    """A class representing implementation of client-related services."""

    def __init__(self, repository: IClientRepository):
        self._repository = repository

    async def register_client(self, client: ClientIn, user_id: UUID) -> ClientDTO:
        """Register a new client in repository and return DTO."""
        record = await self._repository.register_client(client, user_id)
        if not record:
            raise ValueError("Failed to register the client. Please try again.")
        return ClientDTO.from_record(record)

    async def get_client(self, user_id: UUID) -> ClientDTO:
        """Get client by user_id from repository and return DTO."""
        record = await self._repository.get_client(user_id)
        if not record:
            raise ValueError(f"No client found with the provided user_id: {user_id}")
        return ClientDTO.from_record(record)

    async def update_client(self, user_id: UUID, data: ClientIn) -> ClientDTO:
        """Update client by user_id and return DTO."""
        record = await self._repository.update_client(user_id, data)
        if not record:
            raise ValueError(f"No client found with the provided user_id: {user_id}")
        return ClientDTO.from_record(record)

    async def delete_client(self, user_id: UUID) -> ClientDTO:
        """Delete client by user_id and return DTO."""
        record = await self._repository.delete_client(user_id)
        if not record:
            raise ValueError(f"No client found with the provided user_id: {user_id}")
        return ClientDTO.from_record(record)

    async def get_all_clients(self) -> Iterable[ClientDTO]:
        """Get all clients from repository and return DTOs."""
        records = await self._repository.get_all_clients()
        return [ClientDTO.from_record(record) for record in records] if records else []
