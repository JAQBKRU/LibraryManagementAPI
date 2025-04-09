"""Module containing lend service implementation."""
from typing import Iterable
from datetime import date

from fastapi import HTTPException
from pydantic import UUID4

from src.core.domain.lend import LendTransaction, LendTransactionIn, LendStatus
from src.core.repositories.ilend import ILendRepository
from src.infrastructure.dto.lenddto import BookLendHistoryResponseDTO, UserLendHistoryResponseDTO
from src.infrastructure.services.ibook import IBookService
from src.infrastructure.services.ilend import ILendService
from src.infrastructure.services.iuser import IUserService


class LendService(ILendService):
    """A class implementing the lend service."""
    _repository: ILendRepository

    def __init__(
            self,
            repository: ILendRepository,
            book_service: IBookService,
            user_service: IUserService
    ) -> None:
        """The initializer of the `lend service`.

        Args:
            repository (ILendRepository): The reference to the lend repository.
            book_service (IBookService): The reference to the book service.
            user_service (IUserService): The reference to the user service.
        """
        self._repository = repository
        self._book_service = book_service
        self._user_service = user_service

    async def get_all(self) -> Iterable[LendTransaction]:
        """The method getting all lend transactions from the repository.

        Returns:
            Iterable[LendTransaction]: All lend transactions.
        """
        return await self._repository.get_all_lends()

    async def get_lend_by_id(self, lend_id: int) -> LendTransaction | None:
        """The method getting a lend transaction by its ID.

        Args:
            lend_id (int): The ID of the lend transaction.

        Returns:
            LendTransaction | None: The lend transaction details or None if not found.
        """
        return await self._repository.get_lend_by_id(lend_id)

    async def add_lend(self, data: LendTransactionIn) -> LendTransaction | None:
        """The method adding a new lend transaction to the repository.

        Args:
            data (LendTransactionIn): The details of the lend transaction.

        Raises:
            HTTPException: If the book or user is not found or if the operation fails.

        Returns:
            LendTransaction | None: The newly created lend transaction or None if failed.
        """
        book = await self._book_service.get_book_by_id(data.book_id)
        if not book:
            raise HTTPException(status_code=400, detail="Book not found")

        user_exists = await self._user_service.get_user_by_id(data.user_id)
        if not user_exists:
            raise HTTPException(status_code=400, detail="User not found")

        new_lend = await self._repository.add_lend(data)

        if not new_lend:
            raise HTTPException(status_code=500, detail="Failed to create lend transaction")

        return new_lend

    async def update_lend(
            self,
            lend_id: int,
            data: LendTransactionIn
    ) -> LendTransaction | None:
        """The method updating an existing lend transaction.

        Args:
            lend_id (int): The ID of the lend transaction to update.
            data (LendTransactionIn): The updated details of the lend transaction.

        Returns:
            LendTransaction | None: The updated lend transaction or None if failed.
        """
        return await self._repository.update_lend(
            lend_id=lend_id,
            data=data,
        )

    async def delete_lend(self, lend_id: int) -> bool:
        """The method deleting a lend transaction by its ID.

        Args:
            lend_id (int): The ID of the lend transaction to delete.

        Returns:
            bool: True if deletion is successful, False otherwise.
        """
        return await self._repository.delete_lend(lend_id)

    async def return_book(
            self,
            user_id: UUID4,
            book_id: int,
            return_date: date
    ) -> bool:
        """The method returning a borrowed book by updating its lend status.

        Args:
            user_id (UUID4): The ID of the user returning the book.
            book_id (int): The ID of the book being returned.
            return_date (date): The date the book is returned.

        Returns:
            bool: True if the return operation is successful, False otherwise.
        """
        user = await self._user_service.get_user_by_id(user_id)
        if not user:
            return False

        book = await self._book_service.get_book_by_id(book_id)
        if not book:
            return False

        lend_id = await self._repository.get_lend_id_by_book_id_and_user_id(user_id, book_id)
        lend = await self._repository.get_lend_by_id(lend_id)
        if not lend:
            return False

        if lend.status == LendStatus.returned.value:
            return False

        if not lend_id:
            return False


        returned_lend = await self._repository.return_book(user_id, book_id, return_date)

        return returned_lend is not None

    async def get_book_lends(self, book_id: int) -> Iterable[LendTransactionIn]:
        """The method getting the lend history of a book.

        Args:
            book_id (int): The ID of the book.

        Returns:
            BookLendHistoryResponseDTO: The lend history of the book.
        """
        return await self._repository.get_book_lends(book_id)


    async def get_user_lends(self, user_id: UUID4) -> UserLendHistoryResponseDTO:
        """The method getting the lend history of a user.

        Args:
            user_id (UUID4): The ID of the user.

        Returns:
            UserLendHistoryResponseDTO: The lend history of the user.
        """
        return await self._repository.get_user_lends(user_id)
