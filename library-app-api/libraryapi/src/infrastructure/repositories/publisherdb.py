"""Module containing publisher repository implementation."""
from typing import Any, Iterable

from asyncpg import Record
from pydantic import UUID4
from sqlalchemy import select

from src.core.repositories.ipublisher import IPublisherRepository
from src.core.domain.publisher import Publisher, PublisherIn
from src.db import publisher_table, database, book_table


class PublisherRepository(IPublisherRepository):
    """Repository class for handling Publisher-related operations."""
    async def get_all_publishers(self) -> Iterable[Any]:
        """Fetch all publishers from the repository.

        Returns:
            Iterable[Any]: A list of Publisher objects.
        """
        query = select(publisher_table).order_by(publisher_table.c.id.asc())
        publishers = await database.fetch_all(query)
        return [Publisher(**dict(publisher)) for publisher in publishers]

    async def get_publisher_by_id(self, publisher_id: int) -> Any | None:
        """Fetch a publisher by its ID from the repository.

        Args:
            publisher_id (int): The ID of the publisher to retrieve.

        Returns:
            Any | None: The Publisher object if found, else None.
        """
        query = select(publisher_table).where(publisher_table.c.id == publisher_id)
        publisher = await database.fetch_one(query)
        if publisher:
            return Publisher(**dict(publisher))
        return None

    async def add_publisher(self, data: PublisherIn) -> Any | None:
        """Add a new publisher to the repository.

        Args:
            data (PublisherIn): The publisher data to be added.

        Returns:
            Any | None: The added Publisher object if successful, else None.
        """
        query = publisher_table.insert().values(**data.model_dump()).returning(publisher_table.c.id)
        new_publisher_id = await database.fetch_val(query)
        new_publisher = await self._get_by_id(new_publisher_id)
        return Publisher(**dict(new_publisher)) if new_publisher else None

    async def update_publisher(self, publisher_id: int, data: PublisherIn) -> Any | None:
        """Update an existing publisher in the repository.

        Args:
            publisher_id (int): The ID of the publisher to be updated.
            data (PublisherIn): The updated publisher data.

        Returns:
            Any | None: The updated Publisher object if successful, else None.

        Raises:
            ValueError: If the publisher with the specified ID does not exist.
        """
        publisher = await self.get_publisher_by_id(publisher_id)
        if not publisher:
            raise ValueError(f"Publisher with ID {publisher_id} not found.")

        if publisher:
            query = (
                publisher_table.update()
                .where(publisher_table.c.id == publisher_id)
                .values(**data.model_dump())
            )
            await database.execute(query)
            updated_publisher = await self.get_publisher_by_id(publisher_id)

            return Publisher(**dict(updated_publisher)) if updated_publisher else None
        return None

    async def delete_publisher(self, publisher_id: int) -> bool:
        """Remove a publisher by its ID from the repository.

        Args:
            publisher_id (int): The ID of the publisher to be removed.

        Returns:
            bool: True if the publisher was deleted successfully, else False.
        """
        query = publisher_table.delete().where(publisher_table.c.id == publisher_id)
        result = await database.execute(query)

        return result > 0 if result is not None else False

    async def get_publisher_by_user_id(self, user_uuid: UUID4) -> Publisher | None:
        """Fetch a publisher by the user's UUID from the repository.

        Args:
            user_uuid (UUID4): The UUID of the user associated with the publisher.

        Returns:
            Publisher | None: The Publisher object if found, else None.
        """
        query = publisher_table.select().where(publisher_table.c.user_id == user_uuid)
        publisher = await database.fetch_one(query)
        if publisher:
            return Publisher(**dict(publisher))

        return None

    async def _get_by_id(self, publisher_id: int) -> Record | None:
        """Fetch a publisher by its ID.

        Args:
            publisher_id (int): The ID of the publisher.

        Returns:
            Record | None: The publisher record if found, else None.
        """
        query = publisher_table.select().where(publisher_table.c.id == publisher_id)

        return await database.fetch_one(query)

    async def is_publisher_assigned_to_books(self, publisher_id: int) -> bool:
        """Check if the publisher is assigned to any books in the repository.

        Args:
            publisher_id (int): The ID of the publisher.

        Returns:
            bool: True if the publisher is assigned to any books, else False.
        """
        query = select(book_table).where(book_table.c.publisher_id == publisher_id)
        result = await database.fetch_one(query)

        return bool(result)