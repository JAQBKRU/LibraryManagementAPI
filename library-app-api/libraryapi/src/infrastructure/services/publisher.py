"""Module containing publisher service implementation."""
from typing import Iterable, Any

from src.core.domain.publisher import Publisher, PublisherIn
from src.core.repositories.ipublisher import IPublisherRepository
from src.infrastructure.services.ipublisher import IPublisherService


class PublisherService(IPublisherService):
    """A class implementing the publisher service."""
    _repository: IPublisherRepository

    def __init__(self, repository: IPublisherRepository) -> None:
        """The initializer of the `publisher service`.

        Args:
            repository (IPublisherRepository): The reference to the publisher repository.
        """
        self._repository = repository

    async def get_all(self) -> Iterable[Publisher]:
        """The method getting all publishers from the repository.

        Returns:
            Iterable[Publisher]: All publishers.
        """
        return await self._repository.get_all_publishers()

    async def get_publisher_by_id(self, publisher_id: int) -> Publisher | None:
        """The method getting a publisher by its ID.

        Args:
            publisher_id (int): The ID of the publisher.

        Returns:
            Publisher | None: The publisher details or None if not found.
        """
        return await self._repository.get_publisher_by_id(publisher_id)

    async def add_publisher(self, data: PublisherIn) -> Any | None:
        """The method adding a new publisher to the repository.

        Args:
            data (PublisherIn): The details of the publisher to add.

        Returns:
            Any | None: The newly added publisher details or None if failed.
        """
        return await self._repository.add_publisher(data)

    async def update_publisher(
            self,
            publisher_id: int,
            data: PublisherIn,
    ) -> Publisher | None:
        """The method updating an existing publisher in the repository.

        Args:
            publisher_id (int): The ID of the publisher to update.
            data (PublisherIn): The updated publisher details.

        Returns:
            Publisher | None: The updated publisher details or None if failed.
        """
        return await self._repository.update_publisher(
            publisher_id=publisher_id,
            data=data,
        )

    async def delete_publisher(self, publisher_id: int) -> bool:
        """The method deleting a publisher by its ID.

        Args:
            publisher_id (int): The ID of the publisher to delete.

        Returns:
            bool: True if deletion is successful, False otherwise.
        """
        return await self._repository.delete_publisher(publisher_id)

    async def is_publisher_assigned_to_books(self, publisher_id):
        """The method checking if the publisher is assigned to any books.

        Args:
            publisher_id (int): The ID of the publisher.

        Returns:
            bool: True if the publisher is assigned to books, False otherwise.
        """
        return await self._repository.is_publisher_assigned_to_books(publisher_id)

    async def get_publisher_by_user_id(self, user_uuid):
        """The method getting a publisher by the user ID.

        Args:
            user_uuid (str): The UUID of the user.

        Returns:
            Publisher | None: The publisher associated with the user or None if not found.
        """
        return await self._repository.get_publisher_by_user_id(user_uuid)