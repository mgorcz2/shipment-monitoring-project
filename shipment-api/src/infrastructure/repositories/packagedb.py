"""A class representing package DB repository."""

from typing import Iterable

from sqlalchemy import delete, insert, select, update

from src.core.domain.shipment import Package, PackageIn
from src.core.repositories.ipackage import IPackageRepository
from src.db import database, packages_table


class PackageRepository(IPackageRepository):
    """Implementation of package repository."""

    async def add_package(self, data: PackageIn, shipment_id: int) -> dict | None:
        query = insert(packages_table).values(
            id=shipment_id,
            weight=data.weight,
            length=data.length,
            width=data.width,
            height=data.height,
            fragile=data.fragile,
        )
        await database.execute(query)
        return await self.get_package_by_id(shipment_id)

    async def get_package_by_id(self, package_id: int) -> dict | None:
        query = select(packages_table).where(packages_table.c.id == package_id)
        record = await database.fetch_one(query)
        return dict(record) if record else None

    async def get_all_packages(self) -> Iterable[dict]:
        query = select(packages_table)
        records = await database.fetch_all(query)
        return [dict(record) for record in records] if records else []

    async def update_package(self, package_id: int, data: Package) -> dict | None:
        query = (
            update(packages_table)
            .where(packages_table.c.id == package_id)
            .values(
                weight=data.weight,
                length=data.length,
                width=data.width,
                height=data.height,
                fragile=data.fragile,
                pickup_scheduled_date=data.pickup_scheduled_date,
                pickup_actual_date=data.pickup_actual_date,
                delivery_scheduled_date=data.delivery_scheduled_date,
                delivery_actual_date=data.delivery_actual_date,
                cancelled_at=data.cancelled_at,
                note=data.note,
            )
        )
        await database.execute(query)
        return await self.get_package_by_id(package_id)

    async def delete_package(self, package_id: int) -> dict | None:
        package = await self.get_package_by_id(package_id)
        if not package:
            return None
        query = delete(packages_table).where(packages_table.c.id == package_id)
        await database.execute(query)
        return package
