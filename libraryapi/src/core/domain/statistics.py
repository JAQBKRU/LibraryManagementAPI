"""Module containing statistics-related domain models."""
from typing import List

from pydantic import BaseModel, ConfigDict

class TopBorrowedBooks(BaseModel):
    """Model representing a top borrowed book."""
    id: int
    title: str
    borrow_count: int

class Statistics(BaseModel):
    """Model representing general statistics, including the top borrowed books."""
    top_books: List[TopBorrowedBooks]

    model_config = ConfigDict(from_attributes=True, extra="ignore")

class MonthlyBorrowedBooks(BaseModel):
    """Model representing monthly statistics on borrowed books."""
    month: str
    borrow_count: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")

class YearSummary(BaseModel):
    """Model representing yearly statistics for the library."""
    year: int
    total_borrows: int
    most_borrowed_book_title: str

    model_config = ConfigDict(from_attributes=True, extra="ignore")

class MonthlyCategoryStats(BaseModel):
    """Model representing the average number of books borrowed per category each month."""
    month: str
    category: str
    average_borrows_per_month: float

    model_config = ConfigDict(from_attributes=True, extra="ignore")