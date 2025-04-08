"""Module containing lend repository abstractions."""
from abc import ABC, abstractmethod
from datetime import date
from typing import Iterable, Any

from pydantic import UUID4

from src.core.domain.lend import LendTransactionIn as Lend, LendTransactionIn
from src.infrastructure.dto.lenddto import UserLendHistoryResponseDTO, BookLendHistoryResponseDTO


class ILendRepository(ABC):
    """An abstract class representing the protocol of the lend repository."""

    @abstractmethod
    async def get_all_lends(self) -> Iterable[Any]:
        """The abstract method to get all lend transactions from the repository.

        Returns:
            Iterable[Any]: A collection of all lend transactions from the repository.
        """

    @abstractmethod
    async def get_lend_by_id(self, lend_id: int) -> Lend | None:
        """The abstract method to get a lend transaction by its ID.

        Args:
            lend_id (int): The ID of the lend transaction.

        Returns:
            Lend | None: The lend transaction details or None if not found.
        """

    @abstractmethod
    async def add_lend(self, data: Lend) -> Any | None:
        """The abstract method to add a new lend transaction to the repository.

        Args:
            data (Lend): The details of the new lend transaction.

        Returns:
            Any | None: The newly added lend transaction or None.
        """

    @abstractmethod
    async def update_lend(self, lend_id: int, data: Lend) -> Any | None:
        """The abstract method to update an existing lend transaction in the repository.

        Args:
            lend_id (int): The ID of the lend transaction to update.
            data (Lend): The updated details of the lend transaction.

        Returns:
            Any | None: The updated lend transaction or None.
        """

    @abstractmethod
    async def delete_lend(self, lend_id: int) -> bool:
        """The abstract method to remove a lend transaction by its ID.

        Args:
            lend_id (int): The ID of the lend transaction to delete.

        Returns:
            bool: True if the lend transaction was deleted successfully, False otherwise.
        """

    @abstractmethod
    async def get_user_lends(self, user_id: UUID4) -> UserLendHistoryResponseDTO:
        """The abstract method to get all lend transactions for a specific user.

        Args:
            user_id (UUID4): The ID of the user to retrieve lend transactions for.

        Returns:
            UserLendHistoryResponseDTO: The user's lend history.
        """

    @abstractmethod
    async def return_book(self, user_id: UUID4, book_id: int, return_date: date) -> bool:
        """The abstract method to mark a book as returned by a user.

        Args:
            user_id (UUID4): The ID of the user returning the book.
            book_id (int): The ID of the book being returned.
            return_date (date): The date the book was returned.

        Returns:
            bool: True if return is successful, else False.
        """

    @abstractmethod
    async def get_lend_id_by_book_id_and_user_id(self, user_id: UUID4, book_id: int) -> Lend | None:
        """The abstract method to retrieve the lend transaction ID by book and user ID.

        Args:
            user_id (UUID4): The ID of the user.
            book_id (int): The ID of the book.

        Returns:
            Lend | None: The lend transaction ID if found, else None.
        """

    @abstractmethod
    async def get_book_lends(self, book_id) -> Iterable[LendTransactionIn]:
        """The abstract method to get all lend transactions for a specific book.

        Args:
            book_id (int): The ID of the book to retrieve lend transactions for.

        Returns:
            Iterable[LendTransactionIn]: The collection of book's lend history.
        """