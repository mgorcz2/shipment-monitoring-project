"""Module containing staff repository abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from uuid import UUID

from src.core.domain.user import StaffIn


class IStaffRepository(ABC):
    """An abstract repository class for staff."""

    @abstractmethod
    async def register_staff(self, staff: StaffIn, user_id: UUID) -> dict | None:
        """Register a new staff member and return joined staff+user dict.

        Args:
            staff (StaffIn): The staff input data.
            user_id (UUID): The related user id.

        Returns:
            dict | None: The joined staff+user dict if registered.
        """

    @abstractmethod
    async def get_staff(self, staff_id: UUID) -> dict | None:
        """Get staff by provided staff id (user_id), joined with user.

        Args:
            staff_id (UUID): UUID of the staff (user_id).

        Returns:
            dict | None: The joined staff+user dict if exists.
        """

    @abstractmethod
    async def delete_staff(self, staff_id: UUID) -> dict | None:
        """Delete staff by provided staff id (user_id), joined with user.

        Args:
            staff_id (UUID): UUID of the staff (user_id).

        Returns:
            dict | None: The joined staff+user dict if deleted.
        """

    @abstractmethod
    async def update_staff(self, staff_id: UUID, data: StaffIn) -> dict | None:
        """Update staff by provided staff id (user_id), joined with user.

        Args:
            staff_id (UUID): UUID of the staff (user_id).
            data (StaffIn): The updated staff details.

        Returns:
            dict | None: The joined staff+user dict if updated.
        """

    @abstractmethod
    async def get_all_staff(self) -> Iterable[dict] | None:
        """Get all staff members, joined with user.

        Returns:
            Iterable[dict] | None: The joined staff+user dicts.
        """
