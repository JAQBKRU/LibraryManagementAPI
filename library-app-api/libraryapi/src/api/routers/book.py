"""A module containing book endpoints."""
from typing import Iterable, Any

from dependency_injector.wiring import inject, Provide
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

from src.infrastructure.utils import consts
from src.container import Container
from src.core.domain.book import Book, BookIn, BookPublisherId
from src.infrastructure.dto.bookdto import BookDTO, BookAvailabilityDTO

from src.infrastructure.services.ibook import IBookService
from src.infrastructure.services.ipublisher import IPublisherService
from src.infrastructure.services.iuser import IUserService

bearer_scheme = HTTPBearer()

router = APIRouter()

@router.post("/create", tags=["Book"], response_model=Book, status_code=201)
@inject
async def create_book(
        book: BookIn,
        service: IBookService = Depends(Provide[Container.book_service]),
        publisher_service: IPublisherService = Depends(Provide[Container.publisher_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding a new book.

    Args:
        book (BookIn): The book data.
        service (IBookService, optional): The injected service dependency.
        publisher_service (IPublisherService, optional): The injected publisher_service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException:
            - 403 if the user is unauthorized (invalid or missing Bearer token).
            - 403 if no publisher account is found for the authenticated user.

    Returns:
        dict: The new book attributes.
    """
    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    publisher = await publisher_service.get_publisher_by_user_id(user_uuid)
    if not publisher:
        raise HTTPException(status_code=403, detail="Unauthorized: No publisher account found for this user.")

    book_data = book.model_dump()
    book_data["publisher_id"] = publisher.id

    new_book = await service.add_book(BookPublisherId(**book_data))
    return new_book if new_book else {}

@router.get("/all", tags=["Book"], response_model=list[BookDTO], status_code=200)
@inject
async def get_all_books(
        service: IBookService = Depends(Provide[Container.book_service]),
) -> Iterable:
    """An endpoint for getting all books.

    Args:
        service (IBookService, optional): The injected service dependency.

    Returns:
        Iterable: The book attributes collection.
    """
    books = await service.get_all()
    return books

@router.get("/{book_id}", tags=["Book"], response_model=BookDTO, status_code=200)
@inject
async def get_book_by_id(
        book_id: int,
        service: IBookService = Depends(Provide[Container.book_service]),
) -> dict | None:
    """An endpoint for getting book by id.

    Args:
        book_id (int): The id of the book.
        service (IBookService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if the book with the provided ID does not exist.

    Returns:
        dict | None: The book details.
    """
    if book := await service.get_book_by_id(book_id):
        return book.model_dump()

    raise HTTPException(status_code=404, detail="Book not found")

@router.put("/{book_id}/", tags=["Book"], response_model=Book, status_code=201)
@inject
async def update_book(
        book_id: int,
        updated_book: BookIn,
        book_service: IBookService = Depends(Provide[Container.book_service]),
        publisher_service: IPublisherService = Depends(Provide[Container.publisher_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating book data.

    Args:
        book_id (int): The id of the book.
        updated_book (BookIn, optional): The updated book details.
        book_service (IBookService, optional): The injected book_service dependency.
        publisher_service (IPublisherService, optional): The injected publisher_service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException:
            - 403 if the user is not authorized (invalid or missing credentials).
            - 404 if the book with the given `book_id` is not found.
            - 404: If the book is marked as deleted (`is_deleted` is True).
            - 403 if the publisher is not the one who created the book (i.e., attempting to update a book from another publisher).

    Returns:
        dict: The updated book details.
    """
    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    existing_book = await book_service.get_book_by_id(book_id=book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")

    if existing_book.is_deleted:
        raise HTTPException(status_code=404, detail="Book not found or deleted")

    publisher = await publisher_service.get_publisher_by_user_id(user_uuid)
    if not publisher:
        raise HTTPException(status_code=403, detail="Unauthorized: You are not a publisher")

    if existing_book.publisher.id != publisher.id:
        raise HTTPException(status_code=403, detail="You can only update your own books")

    await book_service.update_book(
        book_id=book_id,
        data=updated_book,
    )

    updated_book_data = {**updated_book.model_dump(), "id": book_id, "publisher_id": publisher.id}
    return updated_book_data

@router.delete("/{book_id}/", tags=["Book"], status_code=204)
@inject
async def delete_book(
        book_id: int,
        service: IBookService = Depends(Provide[Container.book_service]),
        publisher_service: IPublisherService = Depends(Provide[Container.publisher_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """An endpoint for deleting book.

    Args:
        book_id (int): The id of the book.
        service (IBookService, optional): The injected service dependency.
        publisher_service (IPublisherService, optional): The injected publisher_service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if the user is unauthorized (invalid token, not a publisher).
        HTTPException: 404 if the book with the given ID is not found.
        HTTPException: 400 if the book is currently borrowed and cannot be deleted.
        HTTPException: 403 if the user is not the publisher of the book.

    Returns:
        None: If successful, the book will be deleted, and no content will be returned.
    """
    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    book = await service.get_book_by_id(book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    publisher = await publisher_service.get_publisher_by_user_id(user_uuid)
    if not publisher:
        raise HTTPException(status_code=403, detail="Unauthorized: You are not a publisher")

    if book.publisher.id != publisher.id:
        raise HTTPException(status_code=403, detail="You can only delete your own books")

    # if await user_service.has_active_lendings(user_id=user_uuid, book_id=book_id):
    #     raise HTTPException(status_code=400, detail="Book is currently borrowed, can not be deleted.")

    await service.delete_book(book_id)
    return

@router.get("/all/books_availability", tags=["Book"], response_model=list[BookAvailabilityDTO], status_code=200)
@inject
async def get_books_availability(
        service: IBookService = Depends(Provide[Container.book_service]),
) -> Iterable:
    """An endpoint for fetching the availability status of all books.

    Args:
        service (IBookService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if no books are found or if the books' availability data cannot be fetched.

    Returns:
        list[BookAvailabilityDTO]: A list of books' availability data.
    """
    if books := await service.get_books_availability():
        return books

    raise HTTPException(status_code=404, detail="Books not found")

@router.get("/{book_title}/search_books_by_title", tags=["Book"], response_model=list[BookDTO], status_code=200)
@inject
async def search_books_by_title(
    title: str,
    service: IBookService = Depends(Provide[Container.book_service]),
) -> Iterable:
    """An endpoint for searching books by title.

    Args:
        title (str): The title of the book to search for.
        service (IBookService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if no books are found with the given title.

    Returns:
        Iterable: A list of books matching the title.
    """
    books = await service.search_books_by_title(title)
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    return books

@router.get("/{book_author}/search_books_by_author", tags=["Book"], response_model=list[BookDTO], status_code=200)
@inject
async def search_books_by_author(
    author: str,
    service: IBookService = Depends(Provide[Container.book_service]),
) -> Iterable:
    """An endpoint for searching books by author.

    Args:
        author (str): The author of the book to search for.
        service (IBookService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if no books are found with the given author.

    Returns:
        Iterable: A list of books matching the author.
    """
    books = await service.search_books_by_author(author)
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    return books