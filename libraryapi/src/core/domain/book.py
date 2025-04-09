"""Module containing book-related domain models"""
from typing import Optional
from pydantic import BaseModel, ConfigDict

class BookIn(BaseModel):
    """Model representing book's DTO attributes."""
    title: str
    author: str
    epoch: str
    genre: str
    kind: str
    publication_year: Optional[str] = None
    language: str
    quantity: int = 1

class BookPublisherId(BookIn):
    """A broker class including publisher in the model."""
    publisher_id: int

class Book(BookIn):
    """Model representing book's attributes in the database."""
    id: Optional[int]
    publisher_id: int
    borrowed_count: int = 0
    is_deleted: bool = False

    model_config = ConfigDict(from_attributes=True, extra="ignore")