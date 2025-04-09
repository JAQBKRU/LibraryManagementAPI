"""Module containing DTO models for lend and lending history."""
from datetime import date
from typing import List, Optional

from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict

from src.infrastructure.dto.bookdto import BookDTO
from src.infrastructure.dto.publisherdto import PublisherDTO
from src.infrastructure.dto.userdto import UserDTO


class LendDTO(BaseModel):
    """A model representing DTO for a lend transaction."""
    user: UserDTO
    lend_id: int
    borrowed_date: date
    returned_date: Optional[date] = None
    status: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "LendDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            LendDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            lend_id=record_dict.get("transaction_id"),  # type: ignore
            user=UserDTO(
                id=record_dict.get("id_1"),  # type: ignore
                name=record_dict.get("name_1"),  # type: ignore
                email=record_dict.get("email_1"),  # type: ignore
                phone=record_dict.get("phone"),  # type: ignore
            ),
            borrowed_date=record_dict.get("borrowed_date"),  # type: ignore
            returned_date=record_dict.get("returned_date") if record_dict.get("returned_date") else None,  # type: ignore
            status=record_dict.get("status"),  # type: ignore
            book=BookDTO(
                id=record_dict.get("book_id"),  # type: ignore
                title=record_dict.get("book_title"),  # type: ignore
                author=record_dict.get("book_author"),  # type: ignore
                epoch=record_dict.get("book_epoch"),  # type: ignore
                genre=record_dict.get("book_genre"),  # type: ignore
                kind=record_dict.get("book_kind"),  # type: ignore
                publication_year=record_dict.get("book_publication_year"),  # type: ignore
                language=record_dict.get("book_language"),  # type: ignore
                borrowed_count=record_dict.get("book_borrowed_count"),  # type: ignore
                publisher=PublisherDTO(
                    id=record_dict.get("publisher_id"),  # type: ignore
                    company_name=record_dict.get("company_name"),  # type: ignore
                    contact_email=record_dict.get("contact_email"),  # type: ignore
                ),
                quantity=record_dict.get("book_quantity"),  # type: ignore
                is_deleted=record_dict.get("book_is_deleted"),  # type: ignore
            ),
        )


class BookLendHistoryResponseDTO(BaseModel):
    """A model representing the response for a book's lend history."""
    book: BookDTO
    history: List[LendDTO]

class UserLendHistoryResponseDTO(BaseModel):
    """A model representing the response for a user's lend history."""
    user: UserDTO
    history: List[BookDTO]
