"""A module providing database access."""
import asyncio
from sqlalchemy.dialects.postgresql import UUID

import databases
import sqlalchemy
from sqlalchemy import Enum
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine
from asyncpg.exceptions import (    # type: ignore
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)

from src.config import config

metadata = sqlalchemy.MetaData()

user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sqlalchemy.text("gen_random_uuid()"),
    ),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("phone", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
)

book_table = sqlalchemy.Table(
    "books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("author", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("publication_year", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("language", sqlalchemy.String),
    sqlalchemy.Column("publisher_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("publishers.id"), nullable=False),
    sqlalchemy.Column("borrowed_count", sqlalchemy.Integer, default=0, nullable=True),
    sqlalchemy.Column("rating", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("categories", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("kind", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("epoch", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("genre", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("quantity", sqlalchemy.Integer, default=1, nullable=False),
    sqlalchemy.Column("is_deleted", sqlalchemy.Boolean, default=False, nullable=False),
)

lend_table = sqlalchemy.Table(
    "lendings",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("book_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("books.id", ondelete="SET NULL")),
    # sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("user_id", UUID(as_uuid=True), sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("borrowed_date", sqlalchemy.Date, nullable=False),
    sqlalchemy.Column("returned_date", sqlalchemy.Date, nullable=True),
    sqlalchemy.Column("status", Enum("borrowed", "returned", name="lend_status"), nullable=False, default="borrowed"),
)

publisher_table = sqlalchemy.Table(
    "publishers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("company_name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("contact_email", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("user_id", UUID(as_uuid=True), sqlalchemy.ForeignKey("users.id"), nullable=False),
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