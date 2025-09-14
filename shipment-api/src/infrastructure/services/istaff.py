"""Module containing staff service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from uuid import UUID

from src.core.domain.user import StaffIn
from src.infrastructure.dto.userDTO import StaffDTO


class IStaffService(ABC):
    """An abstract class representing the protocol of staff service."""

    @abstractmethod
    async def register_staff(self, staff: StaffIn, user_id: UUID) -> StaffDTO:
        """Register a new staff member.

        Args:
            staff (StaffIn): The staff input data to register.
            user_id (UUID): The related user id.

        Returns:
            StaffDTO: The registered staff object if successful.
        """

    @abstractmethod
    async def get_staff(self, user_id: UUID) -> StaffDTO:
        """Get staff by user_id.

        Args:
            user_id (UUID): UUID of the user.

        Returns:
            StaffDTO: The staff object if exists.
        """

    @abstractmethod
    async def update_staff(self, user_id: UUID, data: StaffIn) -> StaffDTO:
        """Update staff by user_id.

        Args:
            user_id (UUID): The user id of the staff.
            data (StaffIn): The updated staff details.

        Returns:
            StaffDTO: The staff object if updated.
        """

    @abstractmethod
    async def delete_staff(self, user_id: UUID) -> StaffDTO:
        """Delete staff by user_id.

        Args:
            user_id (UUID): The user id of the staff.

        Returns:
            StaffDTO: The deleted staff object.
        """

    @abstractmethod
    async def get_all_staff(self) -> Iterable[StaffDTO]:
        """Get all staff members.

        Returns:
            Iterable[StaffDTO]: The staff objects DTO details.
        """
