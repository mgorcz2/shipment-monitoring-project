"""Module containing staff service implementation."""

from typing import Iterable
from uuid import UUID

from src.core.domain.user import StaffIn, UserIn
from src.core.repositories.istaff import IStaffRepository
from src.core.repositories.iuser import IUserRepository
from src.db import database
from src.infrastructure.dto.userDTO import StaffDTO
from src.infrastructure.services.istaff import IStaffService


class StaffService(IStaffService):
    """A class representing implementation of staff-related services."""

    def __init__(
        self, staff_repository: IStaffRepository, user_repository: IUserRepository
    ):
        self._repository = staff_repository
        self._user_repository = user_repository

    async def register_staff_with_user(
        self, staff: StaffIn, user_data: UserIn
    ) -> StaffDTO:
        """Register a new staff member in repository and return DTO."""
        async with database.transaction():
            try:
                user = await self._user_repository.register_user(user_data)
            except Exception as e:
                raise ValueError("User registration failed")
            record = await self._repository.register_staff(staff, user.id)
            if not record:
                raise ValueError(
                    "Failed to register the staff member. Please try again."
                )
            return StaffDTO.from_record(record)

    async def get_staff(self, user_id: UUID) -> StaffDTO:
        """Get staff by user_id from repository and return DTO."""
        record = await self._repository.get_staff(user_id)
        if not record:
            raise ValueError(f"No staff found with the provided user_id: {user_id}")
        return StaffDTO.from_record(record)

    async def update_staff(self, user_id: UUID, data: StaffIn) -> StaffDTO:
        """Update staff by user_id and return DTO."""
        record = await self._repository.update_staff(user_id, data)
        if not record:
            raise ValueError(f"No staff found with the provided user_id: {user_id}")
        return StaffDTO.from_record(record)

    async def delete_staff(self, user_id: UUID) -> StaffDTO:
        """Delete staff by user_id and return DTO."""
        record = await self._repository.delete_staff(user_id)
        if not record:
            raise ValueError(f"No staff found with the provided user_id: {user_id}")
        return StaffDTO.from_record(record)

    async def get_all_staff(self) -> Iterable[StaffDTO]:
        """Get all staff members from repository and return DTOs."""
        records = await self._repository.get_all_staff()
        return [StaffDTO.from_record(record) for record in records] if records else []
