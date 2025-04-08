"""Module containing book service abstractions."""
from abc import ABC, abstractmethod
from typing import Iterable, Any

from src.core.domain.book import Book, BookIn
from src.infrastructure.dto.bookdto import BookDTO, BookAvailabilityDTO


class IBookService(ABC):
    """A class representing book service abstractions."""
    @abstractmethod
    async def get_all(self) -> Iterable[BookDTO]:
        """The method getting all books from the service.

        Returns:
            Iterable[BookDTO]: All books available.
        """

    @abstractmethod
    async def get_book_by_id(
            self,
            book_id: int,
            include_deleted: bool = False
    ) -> BookDTO | None:
        """The method getting a book by its ID.

        Args:
            book_id (int): The ID of the book.
            include_deleted (bool, optional): Whether to include deleted books. Defaults to False.

        Returns:
            BookDTO | None: The details of the book if found, otherwise None.
        """

    @abstractmethod
    async def add_book(self, data: BookIn) -> BookDTO | None:
        """The method adding a new book.

        Args:
            data (BookIn): The data of the book to be added.

        Returns:
            BookDTO | None: The added book details, or None if failed.
        """

    @abstractmethod
    async def update_book(
            self,
            book_id: int,
            data: BookIn,
    ) -> Book | None:
        """The method updating an existing book.

        Args:
            book_id (int): The ID of the book to update.
            data (BookIn): The updated data of the book.

        Returns:
            Book | None: The updated book if successful, otherwise None.
        """

    @abstractmethod
    async def delete_book(self, book_id: int) -> bool:
        """The method deleting a book.

        Args:
            book_id (int): The ID of the book to be deleted.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def increment_borrowed_count(self, book_id: int) -> None:
        """The method incrementing the borrowed count for a book.

        Args:
            book_id (int): The ID of the book to increment the borrowed count.
        """

    @abstractmethod
    async def get_books_availability(self) -> BookAvailabilityDTO:
        """The method getting the availability of all books.

        Returns:
            BookAvailabilityDTO: The availability details of all books.
        """

    @abstractmethod
    async def search_books_by_title(self, title: str) -> Iterable[Any]:
        """Searches for books by title.

        Args:
            title (str): The title or partial title of the book.

        Returns:
            Iterable[Any]: A list of books whose titles match the query.
        """

    @abstractmethod
    async def search_books_by_author(self, author: str) -> Iterable[Any]:
        """Searches for books by author.

        Args:
            author (str): The author's name or part of it.

        Returns:
            Iterable[Any]: A list of books whose authors match the query.
        """