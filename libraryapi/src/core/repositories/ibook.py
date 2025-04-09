"""Module containing book repository abstractions."""
from abc import ABC, abstractmethod
from typing import Iterable, Any
from src.core.domain.book import Book, BookIn
from src.infrastructure.dto.bookdto import BookAvailabilityDTO


class IBookRepository(ABC):
    """An abstract class representing the protocol of the book repository."""

    @abstractmethod
    async def get_all_books(self) -> Iterable[Any]:
        """The abstract method to get all books from the data storage.

        Returns:
            Iterable[Any]: A collection of books from the data storage.
        """

    @abstractmethod
    async def get_book_by_id(self, book_id: int, include_deleted: bool = False) -> Book | None:
        """The abstract method to get a book by its ID.

        Args:
            book_id (int): The ID of the book.
            include_deleted (bool): Whether to include deleted books in the result.

        Returns:
            Book | None: The book details or None if not found.
        """

    @abstractmethod
    async def add_book(self, book: BookIn) -> None:
        """The abstract method to add a new book to the data storage.

        Args:
            book (BookIn): The details of the book to be added.

        Returns:
            None
        """

    @abstractmethod
    async def update_book(self, book_id: int, data: BookIn) -> Book:
        """The abstract method to update an existing book in the data storage.

        Args:
            book_id (int): The ID of the book to be updated.
            data (BookIn): The new details of the book.

        Returns:
            Book: The updated book details.
        """

    @abstractmethod
    async def delete_book(self, book_id: int) -> bool:
        """The abstract method to remove a book by its ID.

        Args:
            book_id (int): The ID of the book to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """

    @abstractmethod
    async def increment_borrowed_count(self, book_id: int) -> None:
        """The abstract method to increment the borrow count of a book.

        Args:
            book_id (int): The ID of the book whose borrow count is to be incremented.

        Returns:
            None
        """

    @abstractmethod
    async def get_books_availability(self) -> BookAvailabilityDTO:
        """The abstract method to get the availability status of books.

        Returns:
            BookAvailabilityDTO: The availability status of the books.
        """

    @abstractmethod
    async def search_books_by_title(self, title: str) -> Iterable[Any]:
        """Searches for books by title.

        Args:
            title (str): The title of the book to search for.

        Returns:
            Iterable[Any]: A collection of books from the data storage.

        Raises:
            HTTPException: If no books are found with the given title.
        """

    @abstractmethod
    async def search_books_by_author(self, author: str) -> Iterable[Any]:
        """Searches for books by author.

        Args:
            author (str): The author of the book to search for.

        Returns:
            Iterable[Any]: A collection of books from the data storage.

        Raises:
            HTTPException: If no books are found with the given author.
        """