"""Module containing lend service abstractions."""
from abc import ABC, abstractmethod
from typing import Iterable, List
from datetime import date

from pydantic import UUID4

from src.core.domain.lend import LendTransactionIn as Lend, LendTransaction


class ILendService(ABC):
    """A class representing lend service abstractions."""
    @abstractmethod
    async def get_all(self) -> Iterable[LendTransaction]:
        """The method getting all lend transactions from the service.

        Returns:
            Iterable[LendTransaction]: All lend transactions.
        """

    @abstractmethod
    async def get_lend_by_id(self, lend_id: int) -> LendTransaction | None:
        """The method getting a lend transaction by its ID.

        Args:
            lend_id (int): The ID of the lend transaction.

        Returns:
            LendTransaction | None: The lend transaction if found, otherwise None.
        """

    @abstractmethod
    async def add_lend(self, data: Lend) -> LendTransaction | None | bool:
        """The method adding a new lend transaction.

        Args:
            data (Lend): The details of the lend transaction to add.

        Returns:
            LendTransaction | None | bool: The added lend transaction if successful,
                                             None or False if failed.
        """

    @abstractmethod
    async def update_lend(
            self,
            lend_id: int,
            data: Lend
    ) -> LendTransaction | None:
        """The method updating an existing lend transaction.

        Args:
            lend_id (int): The ID of the lend transaction to update.
            data (Lend): The updated details of the lend transaction.

        Returns:
            LendTransaction | None: The updated lend transaction if successful, otherwise None.
        """

    @abstractmethod
    async def delete_lend(self, lend_id: int) -> bool:
        """The method deleting a lend transaction.

        Args:
            lend_id (int): The ID of the lend transaction to delete.

        Returns:
            bool: Success of the operation, True if successful, False if not found.
        """

    @abstractmethod
    async def return_book(
            self,
            user_id: UUID4,
            book_id: int,
            return_date: date
    ) -> bool:
        """The method returning a book by updating the status of the lend transaction to 'returned'.

        Args:
            user_id (UUID4): The ID of the user returning the book.
            book_id (int): The ID of the book being returned.
            return_date (date): The date of the return.

        Returns:
            bool: True if the return was successful, False if not found or operation failed.
        """

    @abstractmethod
    async def get_book_lends(self, book_id: int) -> List[LendTransaction]:
        """The method getting all lend transactions for a specific book.

        Args:
            book_id (int): The ID of the book.

        Returns:
            List[LendTransaction]: The list of lend transactions for the given book.
        """

    @abstractmethod
    async def get_user_lends(self, user_id: UUID4) -> Iterable[LendTransaction]:
        """The method getting the lend history of a specific user.

        Args:
            user_id (UUID4): The ID of the user.

        Returns:
            Iterable[LendTransaction]: The list of lend transactions for the given user.
        """
