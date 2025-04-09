"""Module containing lend repository implementation."""
from datetime import date
from typing import Any, Iterable
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import select

from src.core.repositories.ilend import ILendRepository
from src.core.domain.lend import LendTransactionIn as Lend, LendStatus
from src.core.domain.lend import LendTransaction as LendTransaction
from src.db import (
    lend_table,
    user_table,
    book_table,
    database, publisher_table,
)
from src.infrastructure.dto.bookdto import BookDTO
from src.infrastructure.dto.lenddto import BookLendHistoryResponseDTO, LendDTO, UserLendHistoryResponseDTO
from src.infrastructure.dto.publisherdto import PublisherDTO
from src.infrastructure.dto.userdto import UserDTO


class LendRepository(ILendRepository):
    """A class that implements methods for managing lend transactions in the repository."""
    async def get_all_lends(self) -> Iterable[Any]:
        """The method retrieves all lend transactions from the data storage.

        Returns:
            Iterable[Any]: List of lend transactions.
        """
        query = (
            select(lend_table)
            .join(user_table, lend_table.c.user_id == user_table.c.id)
            .join(book_table, lend_table.c.book_id == book_table.c.id)
        )
        lends = await database.fetch_all(query)

        return [LendTransaction(**dict(lend)) for lend in lends]

    async def get_lend_by_id(self, lend_id: int) -> LendTransaction | None:
        """The method retrieves a lend transaction by its ID.

        Args:
            lend_id (int): The ID of the lend transaction.

        Returns:
            LendTransaction | None: The lend transaction if found, else None.
        """
        query = select(lend_table).where(lend_table.c.id == lend_id)
        lend = await database.fetch_one(query)

        if lend:
            lend_data = dict(lend)
            lend_data["status"] = LendStatus(lend_data["status"])

            return LendTransaction(**lend_data)

        return None

    async def add_lend(self, data: Lend) -> Lend | None:
        """The method adds a new lend transaction to the repository.

        Args:
            data (Lend): The lend transaction data.

        Returns:
            Lend | None: The added lend transaction if successful, else None.
        """
        book_exist_query = select(book_table.c.id).where(book_table.c.id == data.book_id)
        book_exists = await database.fetch_one(book_exist_query)
        if not book_exists:
            return None
            # return {"success": False, "message": "Book does not exist."}

        book_quantity_query = select(book_table.c.id, book_table.c.quantity).where(book_table.c.id == data.book_id)
        quantity_exists = await database.fetch_one(book_quantity_query)
        if not quantity_exists or quantity_exists['quantity'] <= 0:
            return None
            # return {"success": False, "message": "Book is out of stock."}

        user_exist_query = select(user_table.c.id).where(user_table.c.id == data.user_id)
        user_exists = await database.fetch_one(user_exist_query)
        if not user_exists:
            return None

        active_lend_query = select(lend_table).where(
            (lend_table.c.user_id == data.user_id) &
            (lend_table.c.book_id == data.book_id) &
            (lend_table.c.status == LendStatus.borrowed.value)
        )
        active_lend = await database.fetch_one(active_lend_query)
        if active_lend:
            return None

        query_lend = lend_table.insert().values(
            **data.model_dump(),
            status=LendStatus.borrowed.value,
            returned_date=None
        )
        new_lend_id = await database.execute(query_lend)

        await database.execute(
            book_table.update().where(book_table.c.id == data.book_id)
            .values(quantity=book_table.c.quantity - 1)
        )

        return await self.get_lend_by_id(new_lend_id)

    async def update_lend(self, lend_id: int, data: Lend) -> Lend | None:
        """The method updates an existing lend transaction.

        Args:
            lend_id (int): The ID of the lend transaction.
            data (Lend): The updated lend transaction data.

        Returns:
            Lend | None: The updated lend transaction if successful, else None.
        """
        query = lend_table.update().where(lend_table.c.id == lend_id).values(**data.model_dump())
        await database.execute(query)
        return await self.get_lend_by_id(lend_id)

    async def delete_lend(self, lend_id: int) -> bool:
        """The method deletes a lend transaction by its ID.

        Args:
            lend_id (int): The ID of the lend transaction to be deleted.

        Returns:
            bool: True if deletion is successful, else False.
        """
        lend = await self.get_lend_by_id(lend_id)
        if not lend:
            raise False

        await database.execute(lend_table.delete().where(lend_table.c.id == lend_id))

        return True

    async def return_book(self, user_id: UUID4, book_id: int, return_date: date) -> bool:
        """The method marks a book as returned.

        Args:
            user_id (UUID4): The user ID returning the book.
            book_id (int): The book ID being returned.
            return_date (date): The date the book is returned.

        Returns:
            bool: True if return is successful, else False.
        """
        lend_id = await self.get_lend_id_by_book_id_and_user_id(user_id, book_id)

        if not lend_id:
            return False

        await database.execute(
            lend_table.update()
            .where(lend_table.c.id == lend_id)
            .values(status=LendStatus.returned.value, returned_date=return_date)  # Enum -> str
        )

        await database.execute(
            book_table.update().where(book_table.c.id == book_id).values(quantity=book_table.c.quantity + 1)
        )

        return True

    async def get_user_lends(self, user_id: UUID4) -> UserLendHistoryResponseDTO:
        """The method retrieves all lend transactions for a specific user.

        Args:
            user_id (UUID4): The user ID.

        Returns:
            UserLendHistoryResponseDTO: The user's lend history.
        """
        query = (
            select(
                lend_table,
                lend_table.c.id.label("transaction_id"),
                user_table.c.id.label("user_id"),
                user_table.c.name.label("name_1"),
                user_table.c.email.label("email_1"),
                user_table.c.phone.label("phone_1"),
                book_table,
                publisher_table.c.id.label("publisher_id"),
                publisher_table.c.company_name.label("company_name"),
                publisher_table.c.contact_email.label("contact_email"),
            )
            .join(user_table, lend_table.c.user_id == user_table.c.id)
            .join(book_table, lend_table.c.book_id == book_table.c.id)
            .join(publisher_table, book_table.c.publisher_id == publisher_table.c.id)
            .where(lend_table.c.user_id == user_id)
            .order_by(lend_table.c.id.asc())
        )
        lends = await database.fetch_all(query)

        if not lends:
            raise HTTPException(status_code=404, detail="No history for this user")

        first_record = dict(lends[0])

        user_details_data = {
            "id": first_record['user_id'],
            "name": first_record['name_1'],
            "email": first_record['email_1'],
            "phone": first_record['phone_1'],
        }
        user_details = UserDTO(**user_details_data)

        history = [BookDTO.from_record(lend) for lend in lends]

        return UserLendHistoryResponseDTO(user=user_details, history=history)

    async def get_book_lends(self, book_id: UUID4) -> BookLendHistoryResponseDTO:
        """The method retrieves all lend transactions for a specific book.

        Args:
            book_id (UUID4): The book ID.

        Returns:
            BookLendHistoryResponseDTO: The book's lend history.
        """
        query = (
            select(
                lend_table,
                lend_table.c.id.label("transaction_id"),
                user_table.c.id.label("id_1"),
                user_table.c.name.label("name_1"),
                user_table.c.email.label("email_1"),
                user_table.c.phone.label("phone"),
                book_table.c.id.label("book_id"),
                book_table.c.title.label("book_title"),
                book_table.c.author.label("book_author"),
                book_table.c.epoch.label("book_epoch"),
                book_table.c.genre.label("book_genre"),
                book_table.c.kind.label("book_kind"),
                book_table.c.publication_year.label("book_publication_year"),
                book_table.c.language.label("book_language"),
                book_table.c.publisher_id.label("book_publisher_id"),
                book_table.c.borrowed_count.label("book_borrowed_count"),
                book_table.c.quantity.label("book_quantity"),
                book_table.c.is_deleted.label("book_is_deleted"),
                publisher_table.c.id.label("publisher_id"),
                publisher_table.c.company_name.label("company_name"),
                publisher_table.c.contact_email.label("contact_email"),
            )
            .join(user_table, lend_table.c.user_id == user_table.c.id)
            .join(book_table, lend_table.c.book_id == book_table.c.id)
            .join(publisher_table, book_table.c.publisher_id == publisher_table.c.id)
            .where(lend_table.c.book_id == book_id)
            .order_by(lend_table.c.id.asc())
        )
        lends = await database.fetch_all(query)

        if not lends:
            raise HTTPException(status_code=404, detail="No history for this book")

        first_record = dict(lends[0])
        book_details_data = {
            "id": first_record["book_id"],
            "title": first_record["book_title"],
            "author": first_record["book_author"],
            "epoch": first_record["book_epoch"],
            "genre": first_record["book_genre"],
            "kind": first_record["book_kind"],
            "publication_year": first_record["book_publication_year"],
            "language": first_record["book_language"],
            "publisher": PublisherDTO(
                id=first_record["publisher_id"],
                company_name=first_record["company_name"],
                contact_email=first_record["contact_email"],
            ),
            "borrowed_count": first_record["book_borrowed_count"],
            "quantity": first_record["book_quantity"],
            "is_deleted": first_record["book_is_deleted"],
        }
        book_details = BookDTO(**book_details_data)

        history = [LendDTO.from_record(lend) for lend in lends]

        return BookLendHistoryResponseDTO(book=book_details, history=history)


    async def get_lend_id_by_book_id_and_user_id(self, user_id: int, book_id: int) -> Lend | None:
        """The method retrieves the latest lend transaction ID for a book and user.

        Args:
            user_id (int): The user ID.
            book_id (int): The book ID.

        Returns:
            Lend | None: The lend transaction ID if found, else None.
        """
        query = (
            select(lend_table.c.id)
            .where(lend_table.c.user_id == user_id)
            .where(lend_table.c.book_id == book_id)
            .order_by(lend_table.c.returned_date.desc())
            .limit(1)
        )

        lend_id = await database.fetch_one(query)

        if lend_id:
            return lend_id["id"]
        return None