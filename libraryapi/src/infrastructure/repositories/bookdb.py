"""Module containing book repository implementation."""
from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, func, case, and_

from src.core.domain.lend import LendStatus
from src.core.repositories.ibook import IBookRepository
from src.core.domain.book import Book, BookIn
from src.db import (
    lend_table,
    publisher_table,
    book_table,
    database,
)

from src.infrastructure.dto.bookdto import BookDTO, BookAvailabilityDTO

class BookRepository(IBookRepository):
    """A class representing book database repository."""
    async def get_all_books(self) -> Iterable[Any]:
        """Retrieve all books from the data storage.

        Returns:
            Iterable[Any]: List of all books in the data storage.
        """

        query = (
            select(
                book_table,
                publisher_table.c.id.label("publisher_id"),
                publisher_table.c.company_name.label("company_name"),
                publisher_table.c.contact_email.label("contact_email")
            )
            .join(publisher_table, book_table.c.publisher_id == publisher_table.c.id)
            .order_by(book_table.c.id.asc())
        )

        books = await database.fetch_all(query)

        return [BookDTO.from_record(book) for book in books]

    async def get_book_by_id(self, book_id: int, include_deleted: bool = False) -> Any | None:
        """Retrieve a book by its ID.

        Args:
            book_id (int): The ID of the book.
            include_deleted (bool): Whether to include deleted books.

        Returns:
            Any | None: The book details or None if not found.
        """

        if not include_deleted:
            query = (
                select(
                    book_table,
                    publisher_table.c.id.label("publisher_id"),
                    publisher_table.c.company_name.label("company_name"),
                    publisher_table.c.contact_email.label("contact_email")
                )
                .join(publisher_table, book_table.c.publisher_id == publisher_table.c.id)
                .where(book_table.c.id == book_id)
            )
        else:
            query = (
                select(
                    book_table,
                    publisher_table.c.id.label("publisher_id"),
                    publisher_table.c.company_name.label("company_name"),
                    publisher_table.c.contact_email.label("contact_email")
                )
                .join(publisher_table, book_table.c.publisher_id == publisher_table.c.id)
                .where(book_table.c.id == book_id, book_table.c.is_deleted == False)
            )

        book = await database.fetch_one(query)

        if book:
            return BookDTO.from_record(book)
        return None

    async def add_book(self, data: BookIn) -> Any | None:
        """Add a new book to the repository.

        Args:
            data (BookIn): The details of the book to be added.

        Returns:
            Any | None: The new book record or None if insertion failed.
        """
        query = book_table.insert().values(**data.model_dump(), borrowed_count=0, is_deleted=False)
        new_book_id = await database.execute(query)
        query = book_table.select().where(book_table.c.id == new_book_id)
        new_book_record = await database.fetch_one(query)
        return new_book_record

    async def update_book(self, book_id: int, data: BookIn) -> Any | None:
        """Update an existing book in the repository.

        Args:
            book_id (int): The ID of the book to update.
            data (BookIn): The updated book details.

        Returns:
            Any | None: The updated book or None if not found.
        """
        book = await database.fetch_one(
            select(book_table).where(
                and_(book_table.c.id == book_id, book_table.c.is_deleted == False)
            )
        )
        if not book:
            return None

        query = (
            book_table.update()
            .where(
                and_(book_table.c.id == book_id, book_table.c.is_deleted == False)
            )
            .values(**data.model_dump())
        )
        await database.execute(query)

        updated_book = await database.fetch_one(
            select(book_table).where(
                and_(book_table.c.id == book_id, book_table.c.is_deleted == False)
            )
        )

        return Book(**dict(updated_book)) if updated_book else None

    async def delete_book(self, book_id: int) -> bool:
        """Mark a book as deleted by its ID.

        Args:
            book_id (int): The ID of the book to delete.

        Returns:
            bool: True if the book was marked as deleted, False otherwise.
        """
        if await self._get_by_id(book_id):
            if await self._is_book_active(book_id):
                # query = book_table \
                #     .delete() \
                #     .where(book_table.c.id == book_id)
                query = (
                    book_table.update()
                    .where(book_table.c.id == book_id)
                    .values(is_deleted=True)
                )
                await database.execute(query)
            return True

        return False

    async def increment_borrowed_count(self, book_id: int) -> None:
        """Increment the borrowed count for a book.

        Args:
            book_id (int): The ID of the book.
        """
        query = (
            book_table.update().where(book_table.c.id == book_id)
            .values(borrowed_count = book_table.c.borrowed_count + 1)
        )
        await database.execute(query)

    async def get_books_availability(self) -> list[BookAvailabilityDTO]:
        """Retrieve availability information for all books.

        Returns:
            List[BookAvailabilityDTO]: List of books with availability details.
        """
        query = (
            select(
                book_table.c.id.label("book_id"),
                book_table.c.title,
                book_table.c.quantity,
                book_table.c.borrowed_count,
                func.count(
                    case(
                        (lend_table.c.returned_date.is_(None), lend_table.c.id)
                    )
                ).label("borrowed"),
                (book_table.c.quantity + func.count(
                    case(
                        (lend_table.c.returned_date.is_(None), lend_table.c.id)
                    )
                )).label("totalStock")
            )
            .order_by(book_table.c.id.asc())
            .join(
                lend_table, lend_table.c.book_id == book_table.c.id, isouter=True
            )
            .group_by(
                book_table.c.id,
                book_table.c.title,
                book_table.c.quantity,
                book_table.c.borrowed_count
            )
            .order_by(book_table.c.id.asc())
        )

        books = await database.fetch_all(query)
        books_availability = [BookAvailabilityDTO.from_record(book) for book in books]
        return books_availability

    async def search_books_by_title(self, title: str) -> Iterable[Any]:
        """Search for books by title.

        Args:
            title (str): The title of the book to search for.

        Returns:
            Iterable[Any]: List of all books matching the title in the data storage.
        """
        query = (
            select(
                book_table,
                publisher_table.c.id.label("publisher_id"),
                publisher_table.c.company_name.label("company_name"),
                publisher_table.c.contact_email.label("contact_email")
            )
            .join(publisher_table, publisher_table.c.id == book_table.c.publisher_id)
            .where(book_table.c.title.ilike(f"%{title}%"))
        )

        books = await database.fetch_all(query)

        return [BookDTO.from_record(book) for book in books]

    async def search_books_by_author(self, author: str) -> Iterable[Any]:
        """Search for books by author.

        Args:
            author (str): The author of the book to search for.

        Returns:
            Iterable[Any]: List of all books matching the author in the data storage.
        """
        query = (
            select(
                book_table,
                publisher_table.c.id.label("publisher_id"),
                publisher_table.c.company_name.label("company_name"),
                publisher_table.c.contact_email.label("contact_email")
            )
            .join(publisher_table, publisher_table.c.id == book_table.c.publisher_id)
            .where(book_table.c.author.ilike(f"%{author}%"))
        )

        books = await database.fetch_all(query)

        return [BookDTO.from_record(book) for book in books]

    async def _get_by_id(self, book_id: int) -> Record | None:
        """Retrieve a book record by ID.

        Args:
            book_id (int): The ID of the book.

        Returns:
            Record | None: The book record or None if not found.
        """
        query = book_table.select().where(book_table.c.id == book_id)
        return await database.fetch_one(query)

    async def _is_book_borrowed(self, book_id) -> bool:
        """Check if a book is currently borrowed.

        Args:
            book_id (int): The ID of the book.

        Returns:
            bool: True if the book is borrowed, False otherwise.
        """
        query = select(
            lend_table
        ) \
        .where(lend_table.c.book_id == book_id) \
        .where(lend_table.c.status == LendStatus.borrowed.value)

        result = await database.fetch_one(query)

        return bool(result)

    async def _is_book_active(self, book_id) -> bool:
        """Check if a book is active (not deleted).

        Args:
            book_id (int): The ID of the book.

        Returns:
            bool: True if the book is active, False otherwise.
        """
        query = (select(book_table)
                 .where(book_table.c.id == book_id)
                 .where(book_table.c.is_deleted == False))

        result = await database.fetch_one(query)

        return bool(result)
