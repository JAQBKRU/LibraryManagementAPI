"""A module containing DTO models for output books and their availability."""
from typing import Optional
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict

from src.infrastructure.dto.publisherdto import PublisherDTO


class BookDTO(BaseModel):
    """A model representing DTO for book data."""
    id: int
    title: str
    author: str
    epoch: str
    genre: str
    kind: str
    publication_year: Optional[str] = None
    language: str
    borrowed_count: int = 0 # Optional[int] = 0
    publisher: PublisherDTO
    quantity: int = 1
    is_deleted: bool = False

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "BookDTO":
        """A method for preparing DTO instance based on a DB record.

        Args:
            record (Record): The DB record.

        Returns:
            BookDTO: The final DTO instance.
        """
        record_dict = dict(record)

        publisher = PublisherDTO(
            id=record_dict.get("publisher_id"),  # type: ignore
            company_name=record_dict.get("company_name"),  # type: ignore
            contact_email=record_dict.get("contact_email")  # type: ignore
        )

        return cls(
            id=record_dict.get("id"),  # type: ignore
            title=record_dict.get("title"),  # type: ignore
            author=record_dict.get("author"),  # type: ignore
            epoch=record_dict.get("epoch"),  # type: ignore
            genre=record_dict.get("genre"),  # type: ignore
            kind=record_dict.get("kind"),  # type: ignore
            publication_year=record_dict.get("publication_year"),  # type: ignore
            language=record_dict.get("language"),  # type: ignore
            borrowed_count=record_dict.get("borrowed_count"),  # type: ignore
            publisher=publisher,
            quantity=record_dict.get("quantity"),
            is_deleted=record_dict.get("is_deleted"),
        )

class BookAvailabilityDTO(BaseModel):
    """A model representing DTO for book availability."""
    book_id: int
    title: str
    totalStock: int
    availableStock: int
    borrowed: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "BookAvailabilityDTO":
        """A method for preparing DTO instance based on a DB record.

        Args:
            record (Record): The DB record.

        Returns:
            BookAvailabilityDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            book_id=record_dict.get("book_id"),  # type: ignore
            title=record_dict.get("title"),  # type: ignore
            totalStock=record_dict.get("totalStock"),  # type: ignore
            availableStock=record_dict.get("quantity"),  # type: ignore
            borrowed=record_dict.get("borrowed"),  # type: ignore
        )