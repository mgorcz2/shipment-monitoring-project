"""Module containing staff repository implementation."""

from typing import Iterable
from uuid import UUID

from sqlalchemy import delete, insert, select, update

from src.core.domain.user import StaffIn
from src.core.repositories.istaff import IStaffRepository
from src.db import database, staff_table, user_table


class StaffRepository(IStaffRepository):
    """A class representing staff DB repository."""

    async def register_staff(self, staff: StaffIn, user_id: UUID) -> dict | None:
        """Register a new staff member and return joined staff+user dict."""
        query = staff_table.insert().values(
            id=user_id,
            first_name=staff.first_name,
            last_name=staff.last_name,
            phone_number=staff.phone_number,
        )
        await database.execute(query)
        return await self.get_staff(user_id)

    async def get_staff(self, staff_id: UUID) -> dict | None:
        """Get staff by provided staff id (user_id), joined with user."""
        query = (
            select(
                staff_table.c.id,
                staff_table.c.first_name,
                staff_table.c.last_name,
                staff_table.c.phone_number,
                user_table.c.email,
                user_table.c.role,
            )
            .join(user_table, staff_table.c.id == user_table.c.id)
            .where(staff_table.c.id == staff_id)
        )
        record = await database.fetch_one(query)
        return dict(record) if record else None

    async def delete_staff(self, staff_id: UUID) -> dict | None:
        """Delete staff by provided staff id (user_id), joined with user."""
        staff = await self.get_staff(staff_id)
        if not staff:
            return None
        query = delete(staff_table).where(staff_table.c.id == staff_id)
        await database.execute(query)
        return staff

    async def update_staff(self, staff_id: UUID, data: StaffIn) -> dict | None:
        """Update staff by provided staff id (user_id), joined with user."""
        query = (
            update(staff_table)
            .where(staff_table.c.id == staff_id)
            .values(data.model_dump())
        )
        await database.execute(query)
        return await self.get_staff(staff_id)

    async def get_all_staff(self) -> Iterable[dict] | None:
        """Get all staff members, joined with user."""
        query = select(
            staff_table.c.id,
            staff_table.c.first_name,
            staff_table.c.last_name,
            staff_table.c.phone_number,
            user_table.c.email,
            user_table.c.role,
        ).join(user_table, staff_table.c.id == user_table.c.id)
        records = await database.fetch_all(query)
        return [dict(record) for record in records] if records else None
