import asyncio

import databases
import sqlalchemy
from asyncpg.exceptions import (  # type: ignore
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import DatabaseError, OperationalError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import func

from shipment_monitoring.config import config
from shipment_monitoring.core.domain.shipment import ShipmentStatus
from shipment_monitoring.core.domain.user import UserRole

metadata = sqlalchemy.MetaData()

shipment_table = sqlalchemy.Table(
    "shipments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("sender_id", sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("courier_id", sqlalchemy.ForeignKey("users.id"), nullable=True),
    sqlalchemy.Column("status", Enum(ShipmentStatus, name="shipment_status")),
    sqlalchemy.Column("weight", sqlalchemy.Float),
    sqlalchemy.Column("recipient_email", sqlalchemy.String, nullable=True),
    sqlalchemy.Column(
        "created_at",
        sqlalchemy.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    sqlalchemy.Column(
        "last_updated",
        sqlalchemy.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
    sqlalchemy.Column("origin", sqlalchemy.String),
    sqlalchemy.Column("destination", sqlalchemy.String),
    sqlalchemy.Column("origin_latitude", sqlalchemy.Float),
    sqlalchemy.Column("origin_longitude", sqlalchemy.Float),
    sqlalchemy.Column("destination_latitude", sqlalchemy.Float),
    sqlalchemy.Column("destination_longitude", sqlalchemy.Float),
)

user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sqlalchemy.text("gen_random_uuid()"),
    ),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True, nullable=False),
    sqlalchemy.Column("password", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("role", Enum(UserRole, name="user_roles")),
)


db_uri = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}/{config.DB_NAME}"
)
engine = create_async_engine(
    db_uri,
    echo=True,
    future=True,
    pool_pre_ping=True,
)
database = databases.Database(
    db_uri,
    force_rollback=True,
)


async def init_db(retries: int = 5, delay: int = 5) -> None:
    """Function initializing the DB.

    Args:
        retries (int, optional): Number of retries of connect to DB.
            Defaults to 5.
        delay (int, optional): Delay of connect do DB. Defaults to 2.
    """
    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all)
            return
        except (
            OperationalError,
            DatabaseError,
            CannotConnectNowError,
            ConnectionDoesNotExistError,
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)

    raise ConnectionError("Could not connect to DB after several retries.")
