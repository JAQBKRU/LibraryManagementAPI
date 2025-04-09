"""Module containing user service implementation."""
from typing import Iterable

from pydantic import UUID4

from src.core.domain.user import UserIn, User
from src.core.repositories.iuser import IUserRepository
from src.infrastructure.dto.tokendto import TokenDTO
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.services.iuser import IUserService
from src.infrastructure.utils.password import verify_password
from src.infrastructure.utils.token import generate_user_token


class UserService(IUserService):
    """A class implementing the user service."""
    _repository: IUserRepository

    def __init__(self, repository: IUserRepository) -> None:
        """The initializer of the `user service`.

        Args:
            repository (IUserRepository): The reference to the user repository.
        """
        self._repository = repository

    async def register_user(self, user: UserIn) -> UserDTO | None:
        """The method registering a new user.

        Args:
            user (UserIn): The input data for the user.

        Returns:
            UserDTO | None: The user data if registration is successful, otherwise None.
        """
        return await self._repository.register_user(user)

    async def authenticate_user(self, user: UserIn) -> TokenDTO | None:
        """The method authenticating a user and generating a token.

        Args:
            user (UserIn): The input data for the user.

        Returns:
            TokenDTO | None: The authentication token if successful, otherwise None.
        """
        if user_data := await self._repository.get_by_email(user.email):
            if verify_password(user.password, user_data.password):
                token_details = generate_user_token(user_data.id)
                # trunk-ignore(bandit/B106)
                return TokenDTO(token_type="Bearer", **token_details)

            return None

        return None

    async def get_by_uuid(self, uuid: UUID4) -> UserDTO | None:
        """The method getting a user by UUID.

        Args:
            uuid (UUID4): The UUID of the user.

        Returns:
            UserDTO | None: The user data if found, otherwise None.
        """
        return await self._repository.get_by_uuid(uuid)

    async def get_by_email(self, email: str) -> UserDTO | None:
        """The method getting a user by email.

        Args:
            email (str): The email of the user.

        Returns:
            UserDTO | None: The user data if found, otherwise None.
        """
        return await self.get_by_email(email)

    async def get_all(self) -> Iterable[UserDTO]:
        """The method getting all users.

        Returns:
            Iterable[UserDTO]: A collection of all users.
        """
        return await self._repository.get_all_users()

    async def get_user_by_id(self, user_uuid: UUID4) -> UserDTO | None:
        """The method getting a user by ID.

        Args:
            user_uuid (UUID4): The UUID of the user.

        Returns:
            UserDTO | None: The user data if found, otherwise None.
        """
        return await self._repository.get_user_by_id(user_uuid)

    # async def add_user(self, data: UserIn) -> User | None:
    #     """The method adding a new user.
    #
    #     Args:
    #         data (UserIn): The input data for the new user.
    #
    #     Returns:
    #         User | None: The newly added user if successful, otherwise None.
    #     """
    #     return await self._repository.add_user(data)

    async def update_user(
            self,
            user_id: int,
            data: UserIn,
    ) -> User | None:
        """The method updating an existing user.

        Args:
            user_id (int): The ID of the user to update.
            data (UserIn): The new data for the user.

        Returns:
            User | None: The updated user data if successful, otherwise None.
        """
        return await self._repository.update_user(
            user_id=user_id,
            data=data,
        )

    async def delete_user(self, user_id: int) -> dict:
        """The method deleting a user by ID.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            dict: A success or error message.
        """
        return await self._repository.delete_user(user_id)

    async def has_active_lendings(self, user_id: UUID4, book_id: int = 0) -> bool:
        """The method checking if the user has active lendings.

        Args:
            user_id (UUID4): The ID of the user.
            book_id (int, optional): The ID of the book. Defaults to 0.

        Returns:
            bool: True if there are active lendings, otherwise False.
        """
        if book_id != 0:
            return await self._repository.has_active_lendings(user_id, book_id)
        return await self._repository.has_active_lendings(user_id)