"""Module containing client service implementation."""

from typing import Iterable
from uuid import UUID

from src.core.domain.user import ClientIn, UserIn
from src.core.repositories.iclient import IClientRepository
from src.core.repositories.iuser import IUserRepository
from src.db import database
from src.infrastructure.dto.userDTO import ClientDTO
from src.infrastructure.email.email_service import EmailService
from src.infrastructure.services.iclient import IClientService
from src.infrastructure.services.iuser import IUserService


class ClientService(IClientService):
    """A class representing implementation of client-related services."""

    def __init__(
        self,
        repository: IClientRepository,
        user_service: IUserService,
        email_service: EmailService,
    ) -> None:
        self._repository = repository
        self._user_service = user_service
        self._email_service = email_service

    async def register_client_with_user(
        self, user_data: UserIn, client: ClientIn
    ) -> ClientDTO:
        """
        Register a new client in repository and return DTO.
        """
        async with database.transaction():
            try:
                user = await self._user_service.register_user(user_data)
            except Exception as e:
                raise ValueError(f"User registration failed: {str(e)}")
            record = await self._repository.register_client(client, user.id)
            if not record:
                raise ValueError("Failed to register the client. Please try again.")
            self._email_service.send_welcome_email(
                user_email=record["email"],
                first_name=record["first_name"],
                address=record["address"],
            )
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
