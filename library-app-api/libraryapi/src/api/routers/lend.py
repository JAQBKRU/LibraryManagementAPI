"""A module containing lend endpoints."""
from datetime import date
from typing import Iterable
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

from src.container import Container
from src.core.domain.lend import LendTransactionIn, LendBroker
from src.core.domain.lend import LendTransaction as LendTransaction
from src.infrastructure.dto.lenddto import BookLendHistoryResponseDTO, UserLendHistoryResponseDTO
from src.infrastructure.services.ibook import IBookService

from src.infrastructure.services.ilend import ILendService
from src.infrastructure.services.iuser import IUserService
from src.infrastructure.utils import consts

bearer_scheme = HTTPBearer()
router = APIRouter()

@router.post("/create", tags=["Lend"], response_model=LendTransaction, status_code=201)
@inject
async def create_lend(
        lend: LendTransactionIn,
        service: ILendService = Depends(Provide[Container.lend_service]),
        book_service: IBookService = Depends(Provide[Container.book_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for creating a new lend transaction.

    Args:
        lend (LendTransactionIn): The details of the lend transaction.
        service (ILendService, optional): The injected service dependency.
        book_service (IBookService, optional): The injected book_service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The authorization credentials.

    Raises:
        HTTPException:
            - 401 if no token is provided.
            - 403 if the user is not authorized.
            - 404 if the book is deleted or not found.
            - 500 if the lend transaction creation fails.

    Returns:
        dict: The new lend transaction details.
    """
    token = credentials.credentials

    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )

    user_uuid = token_payload.get("sub")

    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Token not provided")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    book = await book_service.get_book_by_id(lend.book_id)
    if not book or book.is_deleted:
        raise HTTPException(status_code=404, detail="Book not available for lending")

    lend_with_user = LendBroker(**lend.model_dump(), user_id=user_uuid)

    new_lend = await service.add_lend(lend_with_user)
    if not new_lend:
        raise HTTPException(status_code=500, detail="Failed to create lend transaction")

    await book_service.increment_borrowed_count(lend.book_id)

    return new_lend.model_dump()


@router.get("/all", tags=["Lend"], response_model=list[LendTransaction], status_code=200)
@inject
async def get_all_lends(
        service: ILendService = Depends(Provide[Container.lend_service]),
) -> Iterable:
    """An endpoint for getting all lend transactions.

    Args:
        service (ILendService, optional): The injected service dependency.

    Returns:
        Iterable: The collection of all lend transactions.
    """
    lends = await service.get_all()
    return lends


@router.get("/{lend_id}", tags=["Lend"], response_model=LendTransaction, status_code=200)
@inject
async def get_lend_by_id(
        lend_id: int,
        service: ILendService = Depends(Provide[Container.lend_service]),
) -> dict:
    """An endpoint for getting a lend transaction by its ID.

    Args:
        lend_id (int): The ID of the lend transaction.
        service (ILendService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if the lend transaction with the given ID is not found.

    Returns:
        dict: The details of the lend transaction.
    """
    if lend := await service.get_lend_by_id(lend_id):
        return lend.model_dump()

    raise HTTPException(status_code=404, detail="Lend not found")

@router.put("/{lend_id}/return", tags=["Lend"], response_model=dict, status_code=200)
@inject
async def return_book(
        book_id: int,
        return_date: date,
        service: ILendService = Depends(Provide[Container.lend_service]),
        user_service: IUserService = Depends(Provide[Container.user_service]),
        book_service: IBookService = Depends(Provide[Container.book_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for returning a borrowed book.

    Args:
        book_id (int): The ID of the book to be returned.
        return_date (date): The date when the book is returned.
        service (ILendService, optional): The injected service dependency.
        user_service (IUserService, optional): The injected user_service dependency.
        book_service (IBookService, optional): The injected book_service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The authorization credentials.

    Raises:
        HTTPException:
            - 401 if no token is provided.
            - 403 if the user is not authorized.
            - 404 if the user or book is not found.
            - 400 if the return transaction fails.

    Returns:
        dict: A message showing the success of the return.
    """
    token = credentials.credentials

    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )

    user_uuid = token_payload.get("sub")

    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Token not provided")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    user = await user_service.get_user_by_id(user_uuid)
    book = await book_service.get_book_by_id(book_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")


    result = await service.return_book(user_uuid, book_id, return_date)
    if result:
        return {"message": "Book successfully returned", "title": book.title, "book_id": book_id}

    raise HTTPException(status_code=400, detail="Failed to return book")


@router.get("/{book_id}/history", tags=["Lend"], response_model=BookLendHistoryResponseDTO, status_code=200)
@inject
async def get_book_lend_history(
        book_id: int,
        service: ILendService = Depends(Provide[Container.lend_service]),
        book_service: IBookService = Depends(Provide[Container.book_service]),
) -> Iterable:
    """An endpoint for fetching the lend history of a specific book.

    Args:
        book_id (int): The ID of the book.
        service (ILendService, optional): The injected service dependency.
        book_service (IBookService, optional): The injected book_service dependency.

    Raises:
        HTTPException: 404 if the book is not found.

    Returns:
        Iterable: The lend history of the specified book.
    """
    book = await book_service.get_book_by_id(book_id, True)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    lends = await service.get_book_lends(book_id)

    return lends

@router.get("/user/{user_id}/lends", tags=["Lend"], response_model=UserLendHistoryResponseDTO, status_code=200)
@inject
async def get_user_lend_history(
        user_id: UUID,
        service: ILendService = Depends(Provide[Container.lend_service]),
        user_service: IUserService = Depends(Provide[Container.user_service]),
) -> Iterable:
    """An endpoint for fetching the lend history of a specific user.

    Args:
        user_id (UUID): The ID of the user.
        service (ILendService, optional): The injected service dependency.
        user_service (IUserService, optional): The injected user_service dependency.

    Raises:
        HTTPException: 404 if the user is not found.

    Returns:
        Iterable: The lend history of the specified user.
    """
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    lends = await service.get_user_lends(user_id)
    return lends