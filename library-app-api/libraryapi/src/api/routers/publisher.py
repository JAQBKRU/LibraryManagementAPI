"""A module containing publisher endpoints."""
from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.container import Container
from src.core.domain.publisher import Publisher, PublisherIn, PublisherBroker

from src.infrastructure.services.ipublisher import IPublisherService
from src.infrastructure.utils import consts

bearer_scheme = HTTPBearer()

router = APIRouter()

@router.post("/create", tags=["Publisher"], response_model=Publisher, status_code=201)
@inject
async def create_publisher(
        publisher: PublisherIn,
        service: IPublisherService = Depends(Provide[Container.publisher_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    ) -> dict:
    """An endpoint for creating a new publisher.

    Args:
        publisher (PublisherIn): The publisher data.
        service (IPublisherService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException:
            - 401 if the token is not provided.
            - 403 if the user is not authorized.
            - 400 if the user already has an existing publisher account.

    Returns:
        dict: The new publisher details.
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

    existing_publisher = await service.get_publisher_by_user_id(user_uuid)

    if existing_publisher:
        raise HTTPException(status_code=400, detail="User can only create one publisher")

    extended_publisher_data = PublisherBroker(
        user_id=user_uuid,
        **publisher.model_dump(),
    )

    new_publisher = await service.add_publisher(extended_publisher_data)
    return {
        "id": new_publisher.id,
        "user_id": new_publisher.user_id,
        "contact_email": new_publisher.contact_email,
        "company_name": new_publisher.company_name,
    }

@router.get("/all", tags=["Publisher"], response_model=list[PublisherIn], status_code=200)
@inject
async def get_all_publishers(
        service: IPublisherService = Depends(Provide[Container.publisher_service]),
) -> Iterable:
    """An endpoint for retrieving all publishers.

    Args:
        service (IPublisherService, optional): The injected service dependency.

    Returns:
        Iterable: A collection of all publishers.
    """
    publishers = await service.get_all()

    return publishers

@router.get("/{publisher_id}", tags=["Publisher"], response_model=PublisherIn, status_code=200)
@inject
async def get_publisher_by_id(
        publisher_id: int,
        service: IPublisherService = Depends(Provide[Container.publisher_service]),
) -> dict | None:
    """An endpoint for retrieving a publisher by their ID.

    Args:
        publisher_id (int): The ID of the publisher.
        service (IPublisherService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if the publisher is not found.

    Returns:
        dict | None: The publisher details.
    """
    if publisher := await service.get_publisher_by_id(publisher_id):
        return publisher.model_dump()

    raise HTTPException(status_code=404, detail="Publisher not found")

@router.put("/", tags=["Publisher"], response_model=PublisherIn, status_code=201)
@inject
async def update_publisher(
        updated_publisher: PublisherIn,
        service: IPublisherService = Depends(Provide[Container.publisher_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating an existing publisher.

    Args:
        updated_publisher (PublisherIn): The updated publisher details.
        service (IPublisherService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException:
            - 401 if the token is not provided.
            - 403 if the user is not authorized.
            - 404 if the publisher is not found.

    Returns:
        dict: The updated publisher details.
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

    publisher = await service.get_publisher_by_user_id(user_uuid=user_uuid)

    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")

    await service.update_publisher(
        publisher_id=publisher.id,
        data=updated_publisher,
    )

    return {**updated_publisher.model_dump(), "id": publisher.id, "user_id": user_uuid}

@router.delete("/", tags=["Publisher"], status_code=204)
@inject
async def delete_publisher(
        service: IPublisherService = Depends(Provide[Container.publisher_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """An endpoint for deleting a publisher.

    Args:
        service (IPublisherService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException:
            - 401 if the token is not provided.
            - 403 if the user is not authorized.
            - 404 if the publisher is not found.
            - 400 if the publisher is assigned to books and cannot be deleted.

    Returns:
        None: If successful, the publisher will be deleted, and no content will be returned.
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

    publisher = await service.get_publisher_by_user_id(user_uuid=user_uuid)

    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")


    if await service.is_publisher_assigned_to_books(publisher.id):
        raise HTTPException(status_code=400, detail="Publisher is assigned to books and cannot be deleted")

    await service.delete_publisher(publisher.id)
    return