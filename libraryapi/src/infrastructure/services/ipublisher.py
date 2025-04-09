"""Module containing publisher service abstractions."""
from abc import ABC, abstractmethod
from typing import Iterable, Any

from src.core.domain.publisher import Publisher, PublisherIn


class IPublisherService(ABC):
    """A class representing publisher service abstractions."""
    @abstractmethod
    async def get_all(self) -> Iterable[Publisher]:
        """The method getting all publishers from the service.

        Returns:
            Iterable[Publisher]: All publishers in the service.
        """

    @abstractmethod
    async def get_publisher_by_id(self, publisher_id: int) -> Publisher | None:
        """The method getting a publisher by its ID.

        Args:
            publisher_id (int): The ID of the publisher.

        Returns:
            Publisher | None: The publisher if found, otherwise None.
        """

    @abstractmethod
    async def add_publisher(self, data: PublisherIn) -> Any | None:
        """The method adding a new publisher to the service.

        Args:
            data (PublisherIn): The details of the publisher to add.

        Returns:
            Any | None: The added publisher if successful, otherwise None.
        """

    @abstractmethod
    async def update_publisher(
            self,
            publisher_id: int,
            data: PublisherIn,
    ) -> Publisher | None:
        """The method updating the details of an existing publisher.

        Args:
            publisher_id (int): The ID of the publisher to update.
            data (PublisherIn): The updated details of the publisher.

        Returns:
            Publisher | None: The updated publisher if successful, otherwise None.
        """

    @abstractmethod
    async def delete_publisher(self, publisher_id: int) -> bool:
        """The method deleting a publisher from the service.

        Args:
            publisher_id (int): The ID of the publisher to delete.

        Returns:
            bool: Success of the operation, True if successful, False if not found.
        """

    @abstractmethod
    async def is_publisher_assigned_to_books(self, publisher_id) -> bool:
        """The method checking if a publisher is assigned to any books.

        Args:
            publisher_id (int): The ID of the publisher.

        Returns:
            bool: True if the publisher is assigned to any books, False otherwise.
        """

    @abstractmethod
    async def get_publisher_by_user_id(self, user_uuid) -> Publisher | None:
        """The method getting a publisher by a user ID.

        Args:
            user_uuid (UUID4): The UUID of the user.

        Returns:
            Publisher | None: The publisher assigned to the user, or None if not found.
        """
