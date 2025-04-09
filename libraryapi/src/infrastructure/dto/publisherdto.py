"""Module containing DTO model for publishers."""
from typing import Optional

from pydantic import BaseModel, ConfigDict
from asyncpg import Record  # type: ignore

class PublisherDTO(BaseModel):
    """A model representing DTO for publisher data."""
    id: int
    company_name: str
    contact_email: Optional[str]

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "PublisherDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            PublisherDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),  # type: ignore
            company_name=record_dict.get("company_name"),  # type: ignore
            contact_email=record_dict.get("contact_email"),  # type: ignore
        )