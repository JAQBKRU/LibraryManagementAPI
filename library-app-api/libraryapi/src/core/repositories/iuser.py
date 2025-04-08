"""Module containing user repository abstractions."""
from abc import ABC, abstractmethod
from typing import Iterable, Any

from pydantic import UUID5, UUID4

from src.core.domain.user import UserIn, User


class IUserRepository(ABC):
    """An abstract class representing the protocol of the user repository."""

    @abstractmethod
    async def register_user(self, user: UserIn) -> Any | None:
        """Registers a new user.

        Args:
            user (UserIn): The user data to register.

        Returns:
            Any | None: The newly registered user, or None if registration fails.
        """

    @abstractmethod
    async def get_by_uuid(self, uuid: UUID5) -> Any | None:
        """Fetches a user by their UUID.

        Args:
            uuid (UUID5): The UUID of the user.

        Returns:
            Any | None: The user associated with the provided UUID, or None if not found.
        """

    @abstractmethod
    async def get_by_email(self, email: str) -> Any | None:
        """Fetches a user by their email.

        Args:
            email (str): The email of the user.

        Returns:
            Any | None: The user associated with the provided email, or None if not found.
        """

    @abstractmethod
    async def get_all_users(self) -> Iterable[Any]:
        """Fetches all users from the repository.

        Returns:
            Iterable[Any]: A collection of all users.
        """

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None:
        """Fetches a user by their ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            User | None: The user associated with the provided ID, or None if not found.
        """

    # @abstractmethod
    # async def add_user(self, data: UserIn) -> Any | None:
    #     """Adds a new user to the repository.
    #
    #     Args:
    #         data (UserIn): The user data to add.
    #
    #     Returns:
    #         Any | None: The newly added user, or None if the addition fails.
    #     """

    @abstractmethod
    async def update_user(self, user_id: int, data: UserIn) -> Any | None:
        """Updates an existing user in the repository.

        Args:
            user_id (int): The ID of the user to update.
            data (UserIn): The updated user data.

        Returns:
            Any | None: The updated user, or None if the update fails.
        """

    @abstractmethod
    async def delete_user(self, user_id: int) -> dict:
        """Removes a user by their ID from the repository.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            dict: A confirmation or the deleted user data.
        """

    @abstractmethod
    async def has_active_lendings(self, user_id: UUID4, book_id: int = 0) -> bool:
        """Checks if a user has active lendings.

        Args:
            user_id (UUID4): The ID of the user.
            book_id (int, optional): The ID of the book to check for active lending (default is 0).

        Returns:
            bool: True if the user has active lendings, False otherwise.
        """