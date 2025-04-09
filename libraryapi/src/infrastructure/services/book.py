"""Module containing book service implementation."""
from typing import Iterable

from src.core.domain.book import Book, BookIn
from src.core.repositories.ibook import IBookRepository
from src.infrastructure.dto.bookdto import BookDTO, BookAvailabilityDTO
from src.infrastructure.services.ibook import IBookService


class BookService(IBookService):
    """A class implementing the book service."""
    _repository: IBookRepository

    def __init__(self, repository: IBookRepository) -> None:
        """The initializer of the `book service`.

        Args:
            repository (IBookRepository): The reference to the book repository.
        """
        self._repository = repository

    async def get_all(self) -> Iterable[BookDTO]:
        """The method getting all books from the repository.

        Returns:
            Iterable[BookDTO]: All books from the repository.
        """
        return await self._repository.get_all_books()

    async def get_book_by_id(
            self,
            book_id: int,
            include_deleted: bool = False
    ) -> BookDTO | None:
        """The method getting a book by its ID from the repository.

        Args:
            book_id (int): The ID of the book.
            include_deleted (bool, optional): Whether to include deleted books. Defaults to False.

        Returns:
            BookDTO | None: The book details or None if the book doesn't exist.
        """
        return await self._repository.get_book_by_id(book_id)

    async def add_book(self, data: BookIn) -> Book | None:
        """The method adding a new book to the repository.

        Args:
            data (BookIn): The details of the new book.

        Returns:
            Book | None: The newly added book or None if the operation fails.
        """
        return await self._repository.add_book(data)

    async def update_book(
            self,
            book_id: int,
            data: BookIn,
    ) -> Book | None:
        """The method updating an existing book in the repository.

        Args:
            book_id (int): The ID of the book to update.
            data (BookIn): The updated details of the book.

        Returns:
            Book | None: The updated book details or None if the operation fails.
        """
        return await self._repository.update_book(
            book_id=book_id,
            data=data,
        )

    async def delete_book(self, book_id: int) -> bool:
        """The method removing a book from the repository.

        Args:
            book_id (int): The ID of the book to delete.

        Returns:
            bool: Success or failure of the deletion operation.
        """
        return await self._repository.delete_book(book_id)

    async def increment_borrowed_count(self, book_id: int) -> None:
        """The method incrementing the borrow count of a book.

        Args:
            book_id (int): The ID of the book.
        """
        await self._repository.increment_borrowed_count(book_id)

    async def get_books_availability(self) -> BookAvailabilityDTO:
        """The method getting the availability details of books.

        Returns:
            BookAvailabilityDTO: The availability details of the books.
        """
        return await self._repository.get_books_availability()

    async def search_books_by_title(self, title: str) -> Iterable[BookDTO]:
        """The method searching for books by title.

        Args:
            title (str): The title of the book to search for.

        Returns:
            Iterable[BookDTO]: All books from repository that match the title.
        """
        return await self._repository.search_books_by_title(title)

    async def search_books_by_author(self, author: str) -> Iterable[BookDTO]:
        """The method searching for books by author.

        Args:
            author (str): The author of the book to search for.

        Returns:
            Iterable[BookDTO]: All books from repository that match the author.
        """
        return await self._repository.search_books_by_author(author)