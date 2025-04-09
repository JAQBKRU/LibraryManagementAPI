"""Module containing publisher repository abstractions."""
from abc import ABC, abstractmethod
from typing import Iterable, Any

from src.core.domain.publisher import Publisher, PublisherIn


class IPublisherRepository(ABC):
    """An abstract class representing the protocol of the publisher repository."""

    @abstractmethod
    async def get_all_publishers(self) -> Iterable[Any]:
        """The abstract method to get all publishers from the repository.

        Returns:
            Iterable[Any]: A collection of all publishers from the repository.
        """

    @abstractmethod
    async def get_publisher_by_id(self, publisher_id: int) -> Publisher | None:
        """The abstract method to get a publisher by its ID.

        Args:
            publisher_id (int): The ID of the publisher.

        Returns:
            Publisher | None: The publisher details or None if not found.
        """

    @abstractmethod
    async def add_publisher(self, data: PublisherIn) -> Publisher | None:
        """The abstract method to add a new publisher to the repository.

        Args:
            data (PublisherIn): The details of the new publisher.

        Returns:
            Publisher | None: The newly added publisher or None.
        """

    @abstractmethod
    async def update_publisher(self, publisher_id: int, data: PublisherIn) -> Any | None:
        """The abstract method to update an existing publisher in the repository.

        Args:
            publisher_id (int): The ID of the publisher to update.
            data (PublisherIn): The updated details of the publisher.

        Returns:
            Any | None: The updated publisher details or None.
        """

    @abstractmethod
    async def delete_publisher(self, publisher_id: int) -> bool:
        """The abstract method to remove a publisher by its ID.

        Args:
            publisher_id (int): The ID of the publisher to delete.

        Returns:
            bool: True if the publisher was deleted successfully, False otherwise.
        """

    @abstractmethod
    async def is_publisher_assigned_to_books(self, publisher_id) -> bool:
        """The abstract method to check if the publisher is assigned to any books.

        Args:
            publisher_id (int): The ID of the publisher.

        Returns:
            bool: True if the publisher is assigned to any books, False otherwise.
        """

    @abstractmethod
    async def get_publisher_by_user_id(self, user_uuid) -> Publisher | None:
        """The abstract method to get a publisher by the user ID who added it.

        Args:
            user_uuid (str): The UUID of the user.

        Returns:
            Publisher | None: The publisher associated with the given user ID.
        """