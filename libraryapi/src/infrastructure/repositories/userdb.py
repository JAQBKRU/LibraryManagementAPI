"""Module containing user repository implementation."""
from typing import Any, Iterable

from asyncpg import Record
from pydantic import UUID5, UUID4
from sqlalchemy import select

from src.core.repositories.iuser import IUserRepository
from src.core.domain.user import User, UserIn
from src.db import (
    lend_table,
    user_table,
    database,
)
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.utils.password import hash_password


class UserRepository(IUserRepository):
    """An implementation of repository class for user."""
    async def register_user(self, user: UserIn) -> Any | None:
        """A method registering new user.

        Args:
            user (UserIn): The user input data.

        Returns:
            Any | None: The new user object or None if the user already exists.
        """
        if await self.get_by_email(user.email):
            return None

        user.password = hash_password(user.password)

        query = user_table.insert().values(**user.model_dump())
        new_user_uuid = await database.execute(query)

        return await self.get_by_uuid(new_user_uuid)

    async def get_by_uuid(self, uuid: UUID5) -> Any | None:
        """A method getting user by UUID.

        Args:
            uuid (UUID5): UUID of the user.

        Returns:
            Any | None: The user object if exists, otherwise None.
        """
        query = user_table \
            .select() \
            .where(user_table.c.id == uuid)
        user = await database.fetch_one(query)

        return user

    async def get_by_email(self, email: str) -> Any | None:
        """A method getting user by email.

        Args:
            email (str): The email of the user.

        Returns:
            Any | None: The user object if exists, otherwise None.
        """
        query = user_table \
            .select() \
            .where(user_table.c.email == email)
        user = await database.fetch_one(query)

        return user

    async def get_all_users(self) -> Iterable[Any]:
        """A method getting all users from the repository.

        Returns:
            Iterable[Any]: List of user objects.
        """
        query = (
            select(user_table)
            .order_by(user_table.c.name.asc())
        )
        users = await database.fetch_all(query)

        return [User(**dict(user)) for user in users]

    async def get_user_by_id(self, user_uuid: UUID4) -> Any | None:
        """A method getting user by ID from the repository.

        Args:
            user_uuid (UUID4): The UUID of the user.

        Returns:
            Any | None: The user object if exists, otherwise None.
        """
        query = select(user_table).where(user_table.c.id == user_uuid)
        user = await database.fetch_one(query)

        if user:
            return UserDTO.from_record(user)
        return None

    # async def add_user(self, data: UserIn) -> Any | None:
    #     """A method adding a new user to the repository.
    #
    #     Args:
    #         data (UserIn): The input data for the new user.
    #
    #     Returns:
    #         Any | None: The newly added user object.
    #     """
    #     query = user_table.insert().values(**data.model_dump())
    #     new_user_id = await database.execute(query)
    #     new_user = await self._get_by_id(new_user_id)
    #
    #     return User(**dict(new_user)) if new_user else None

    async def update_user(self, user_id: UUID4, data: UserIn) -> Any | None:
        """A method updating an existing user in the repository.

        Args:
            user_id (UUID4): The UUID of the user to update.
            data (UserIn): The data to update the user with.

        Returns:
            Any | None: The updated user object, or None if the user doesn't exist.
        """
        if await self._get_by_id(user_id):
            if data.password:
                hashed_password = hash_password(data.password)
                data.password = hashed_password
            query = (
                user_table.update()
                .where(user_table.c.id == user_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            user = await self._get_by_id(user_id)

            return User(**dict(user)) if user else None

        return None

    async def delete_user(self, user_id: UUID4) -> dict:
        """A method removing a user by its ID from the repository.

        Args:
            user_id (UUID4): The UUID of the user to delete.

        Returns:
            dict: Success message or error if the user has active lendings.
        """
        lendings_query = select(lend_table).where(lend_table.c.user_id == user_id)
        has_lendings = await database.fetch_one(lendings_query)
        if has_lendings:
            return {"success": False, "message": "Can not delete user: User has active lendings"}

        await self._get_by_id(user_id)
        query = user_table \
                .delete() \
                .where(user_table.c.id == user_id)
        await database.execute(query)
        return {"success": True, "message": "User deleted successfully."}

    async def _get_by_id(self, user_id: int) -> Record | None:
        """A method getting user by ID from the repository.

        Args:
            user_id (int): The ID of the user.

        Returns:
            Record | None: The user record if found, otherwise None.
        """
        query = user_table.select().where(user_table.c.id == user_id).order_by(user_table.c.id.asc())
        return await database.fetch_one(query)

    async def has_active_lendings(self, user_id: int, book_id: int = 0) -> bool:
        """A method checking if a user has active lendings.

        Args:
            user_id (int): The ID of the user to check.
            book_id (int, optional): The ID of the book to check for lendings. Defaults to 0.

        Returns:
            bool: True if the user has active lendings, otherwise False.
        """
        if user_id != 0:
            query = select(lend_table).where(lend_table.c.user_id == user_id, lend_table.c.book_id == book_id, lend_table.c.returned_date.is_(None))
        else:
            query = select(lend_table).where(lend_table.c.book_id == book_id)
        result = await database.fetch_one(query)
        return result