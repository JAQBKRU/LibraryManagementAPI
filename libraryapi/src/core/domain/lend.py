"""Module containing lend-related domain models."""
from datetime import date

from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, UUID4


class LendStatus(str, Enum):
    """Enum class representing the possible statuses of a lend transaction."""
    borrowed = "borrowed"
    returned = "returned"

class LendTransactionIn(BaseModel):
    """Model representing the input attributes for a lend transaction."""
    book_id: int
    borrowed_date: date

class LendTransaction(LendTransactionIn):
    """Model representing a lend transaction with extended attributes for the database."""
    id: int
    user_id: Optional[UUID]
    status: LendStatus = LendStatus.borrowed
    returned_date: Optional[date] = None

    class Config:
        """Configuration for the LendTransaction model."""
        orm_mode = True
        from_attributes = True
        extra = "ignore"

class LendBroker(LendTransactionIn):
    """A broker class that includes the user_id in the lend transaction model."""
    user_id: UUID4