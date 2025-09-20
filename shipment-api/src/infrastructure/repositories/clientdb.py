"""Module containing client repository implementation."""

from typing import Iterable
from uuid import UUID

from sqlalchemy import delete, insert, select, update

from src.core.domain.user import Client, ClientIn
from src.core.repositories.iclient import IClientRepository
from src.db import client_table, database, user_table


class ClientRepository(IClientRepository):
    """A class representing client DB repository."""

    async def register_client(self, client: ClientIn, user_id: UUID) -> dict | None:
        """Register a new client and return joined client+user dict."""
        query = client_table.insert().values(
            id=user_id,
            first_name=client.first_name,
            last_name=client.last_name,
            phone_number=client.phone_number,
            address=client.address,
        )
        await database.execute(query)
        return await self.get_client(user_id)

    async def get_client(self, client_id: UUID) -> dict | None:
        """Get client by provided client id (user_id), joined with user."""
        query = (
            select(
                client_table.c.id,
                client_table.c.first_name,
                client_table.c.last_name,
                client_table.c.phone_number,
                client_table.c.address,
                user_table.c.email,
                user_table.c.role,
            )
            .join(user_table, client_table.c.id == user_table.c.id)
            .where(client_table.c.id == client_id)
        )
        record = await database.fetch_one(query)
        return dict(record) if record else None

    async def delete_client(self, client_id: UUID) -> dict | None:
        """Delete client by provided client id (user_id), joined with user."""
        client = await self.get_client(client_id)
        if not client:
            return None
        query = delete(client_table).where(client_table.c.id == client_id)
        await database.execute(query)
        return client

    async def update_client(self, client_id: UUID, data: ClientIn) -> dict | None:
        """Update client by provided client id (user_id), joined with user."""
        query = (
            update(client_table)
            .where(client_table.c.id == client_id)
            .values(data.model_dump())
        )
        await database.execute(query)
        return await self.get_client(client_id)

    async def get_all_clients(self) -> Iterable[dict] | None:
        """Get all clients, joined with user."""
        query = select(
            client_table.c.id,
            client_table.c.first_name,
            client_table.c.last_name,
            client_table.c.phone_number,
            client_table.c.address,
            user_table.c.email,
            user_table.c.role,
        ).join(user_table, client_table.c.id == user_table.c.id)
        records = await database.fetch_all(query)
        return [dict(record) for record in records] if records else None
