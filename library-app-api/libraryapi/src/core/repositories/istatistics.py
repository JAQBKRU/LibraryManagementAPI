"""Module containing statistics repository abstractions."""
from abc import ABC, abstractmethod
from typing import List

from src.core.domain.statistics import TopBorrowedBooks, MonthlyBorrowedBooks, YearSummary, MonthlyCategoryStats


class IStatisticsRepository(ABC):
    """An abstract class representing the protocol of the statistics repository."""

    @abstractmethod
    async def get_top_borrowed_books(self) -> List[TopBorrowedBooks]:
        """The abstract method to get a list of the top borrowed books.

        Returns:
            List[TopBorrowedBooks]: A list of top borrowed books.
        """

    @abstractmethod
    async def get_monthly_borrowed_books(self) -> List[MonthlyBorrowedBooks]:
        """The abstract method to get a list of books borrowed on a monthly basis.

        Returns:
            List[MonthlyBorrowedBooks]: A list of books with their respective monthly borrow counts.
        """

    @abstractmethod
    async def get_year_summary(self, year: int) -> YearSummary:
        """The abstract method to get the summary of book borrowing for a specific year.

        Args:
            year (int): The year for which the summary is requested.

        Returns:
            YearSummary: The summary of book borrowing for the given year.
        """

    @abstractmethod
    async def get_average_borrowed_per_category_monthly(self) -> List[MonthlyCategoryStats]:
        """The abstract method to get the average number of books borrowed per category each month.

        Returns:
            List[MonthlyCategoryStats]: A list of monthly statistics for each category, including the average borrows per month.
        """