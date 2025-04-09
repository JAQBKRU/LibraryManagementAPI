"""A module containing user management endpoints."""
from typing import Iterable
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import Depends, APIRouter, HTTPException

from src.container import Container
from src.core.domain.user import User, UserIn, UserAuth
from src.infrastructure.dto.tokendto import TokenDTO
from src.infrastructure.dto.userdto import UserDTO

from src.infrastructure.services.iuser import IUserService

router = APIRouter()

@router.post("/register", tags=["User"], response_model=UserDTO, status_code=201)
@inject
async def register_user(
        user: UserIn,
        service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """An endpoint for registering a new user.

    Args:
        user (UserIn): The user registration data.
        service (IUserService, optional): The injected service dependency.

    Raises:
        HTTPException:
            - 400 if the user with the provided email already exists.

    Returns:
        UserDTO: The details of the newly registered user.
    """
    if new_user := await service.register_user(user):
        return UserDTO(**dict(new_user)).model_dump()

    raise HTTPException(status_code=400, detail="The user with provided e-mail already exists")


@router.post("/token", tags=["User"], response_model=TokenDTO, status_code=200)
@inject
async def authenticate_user(
        user: UserAuth,
        service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """An endpoint for authenticating a user and generating a token.

    Args:
        user (UserAuth): The user's login credentials.
        service (IUserService, optional): The injected service dependency.

    Raises:
        HTTPException:
            - 401 if the provided credentials are incorrect.

    Returns:
        TokenDTO: The authentication token.
    """
    if token_details := await service.authenticate_user(user):
        print("user confirmed")
        return token_details.model_dump()

    raise HTTPException(status_code=401, detail="Provided incorrect credentials")

# @router.post("/create", tags=["User"], response_model=User, status_code=201)
# @inject
# async def create_user(
#         user: UserIn,
#         service: IUserService = Depends(Provide[Container.user_service])
#     ) -> dict:
#     """An endpoint for creating a new user in the system.
#
#     Args:
#         user (UserIn): The user creation data.
#         service (IUserService, optional): The injected service dependency.
#
#     Returns:
#         dict: The newly created user details.
#     """
#     new_user = await service.add_user(user)
#     return new_user.model_dump() if new_user else {}

@router.get("/all", tags=["User"], response_model=list[UserDTO], status_code=200)
@inject
async def get_all_users(
        service: IUserService = Depends(Provide[Container.user_service]),
) -> Iterable:
    """An endpoint for retrieving all users in the system.

    Args:
        service (IUserService, optional): The injected service dependency.

    Raises:
        HTTPException:
            - 404 if no users are found.

    Returns:
        list: A list of all users in the system.
    """
    users = await service.get_all()
    if not users:
        raise HTTPException(status_code=404, detail="No data")
    return users

@router.get("/{user_id}", tags=["User"], response_model=UserDTO, status_code=200)
@inject
async def get_user_by_uuid(
        user_id: UUID,
        service: IUserService = Depends(Provide[Container.user_service]),
) -> dict | None:
    """An endpoint for fetching a user by their UUID.

    Args:
        user_id (UUID): The unique identifier of the user.
        service (IUserService, optional): The injected service dependency.

    Raises:
        HTTPException:
            - 404 if the user is not found.

    Returns:
        dict: The user details corresponding to the provided UUID.
    """
    if user := await service.get_user_by_id(user_id):
        return user.model_dump()

    raise HTTPException(status_code=404, detail="User not found")

# @router.put("/{user_id}/", tags=["User"], response_model=User, status_code=201)
# @inject
# async def update_user(
#         user_id: UUID,
#         updated_user: UserIn,
#         service: IUserService = Depends(Provide[Container.user_service]),
# ) -> dict:
#     """An endpoint for updating an existing user's data.
#
#     Args:
#         user_id (UUID): The unique identifier of the user to be updated.
#         updated_user (UserIn): The updated user data.
#         service (IUserService, optional): The injected service dependency.
#
#     Raises:
#         HTTPException:
#             - 404 if the user is not found.
#
#     Returns:
#         dict: The updated user details.
#     """
#     if await service.get_user_by_id(user_uuid=user_id):
#         await service.update_user(user_id=user_id, data=updated_user)
#
#         return {**updated_user.model_dump(), "id": user_id}
#
#     raise HTTPException(status_code=404, detail="User not found")
#
# @router.delete("/{user_id}/", tags=["User"], status_code=204)
# @inject
# async def delete_user(
#         user_id: UUID,
#         service: IUserService = Depends(Provide[Container.user_service]),
# ) -> None:
#     """An endpoint for deleting a user from the system.
#
#     Args:
#         user_id (UUID): The unique identifier of the user to be deleted.
#         service (IUserService, optional): The injected service dependency.
#
#     Raises:
#         HTTPException:
#             - 404 if the user is not found.
#             - 400 if the user has active lendings and cannot be deleted.
#
#     Returns:
#         None
#     """
#     if await service.get_user_by_id(user_uuid=user_id):
#         if await service.has_active_lendings(user_id=user_id):
#             raise HTTPException(status_code=400, detail="Can not delete user: User has active lendings.")
#
#         await service.delete_user(user_id)
#         return
#
#     raise HTTPException(status_code=404, detail="User not found")
