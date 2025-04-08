"""Module containing user service abstractions."""
from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID5
from pydantic.v1 import UUID4

from src.core.domain.user import User, UserIn, UserAuth
from src.infrastructure.dto.tokendto import TokenDTO
from src.infrastructure.dto.userdto import UserDTO


class IUserService(ABC):
    """A class representing user service abstractions."""
    @abstractmethod
    async def register_user(self, user: UserIn) -> UserDTO | None:
        """The method registers a new user.

        Args:
            user (UserIn): The details of the user to register.

        Returns:
            UserDTO | None: The registered user details or None if registration fails.
        """

    @abstractmethod
    async def authenticate_user(self, user: UserAuth) -> TokenDTO | None:
        """The method authenticates a user and returns a token.

        Args:
            user (UserAuth): The user's credentials (email and password).

        Returns:
            TokenDTO | None: The generated authentication token or None if authentication fails.
        """

    @abstractmethod
    async def get_by_uuid(self, uuid: UUID5) -> UserDTO | None:
        """The method gets a user by their UUID.

        Args:
            uuid (UUID5): The unique identifier of the user.

        Returns:
            UserDTO | None: The user details or None if no user is found.
        """

    @abstractmethod
    async def get_by_email(self, email: str) -> UserDTO | None:
        """The method gets a user by their email.

        Args:
            email (str): The email address of the user.

        Returns:
            UserDTO | None: The user details or None if no user is found.
        """

    @abstractmethod
    async def get_all(self) -> Iterable[UserDTO]:
        """The method gets all users.

        Returns:
            Iterable[UserDTO]: A list of all user details.
        """

    @abstractmethod
    async def get_user_by_id(self, user_uuid: UUID4) -> UserDTO | None:
        """The method gets a user by their UUID.

        Args:
            user_uuid (UUID4): The unique identifier of the user.

        Returns:
            UserDTO | None: The user details or None if no user is found.
        """

    # @abstractmethod
    # async def add_user(self, data: UserIn) -> User | None:
    #     """The method adds a new user.
    #
    #     Args:
    #         data (UserIn): The details of the user to add.
    #
    #     Returns:
    #         User | None: The added user details or None if adding the user fails.
    #     """

    @abstractmethod
    async def update_user(
            self,
            user_id: UUID4,
            data: UserIn,
    ) -> User | None:
        """The method updates an existing user.

        Args:
            user_id (UUID4): The ID of the user to update.
            data (UserIn): The updated user details.

        Returns:
            User | None: The updated user details or None if the update fails.
        """

    @abstractmethod
    async def delete_user(self, user_id: UUID4) -> bool:
        """The method deletes a user.

        Args:
            user_id (UUID4): The ID of the user to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """

    @abstractmethod
    async def has_active_lendings(
            self,
            user_id: UUID4,
            book_id: int = 0
    ) -> bool:
        """The method checks if the user has active lendings.

        Args:
            user_id (UUID4): The ID of the user.
            book_id (int, optional): The ID of the book to check, defaults to 0.

        Returns:
            bool: True if the user has active lendings, False otherwise.
        """