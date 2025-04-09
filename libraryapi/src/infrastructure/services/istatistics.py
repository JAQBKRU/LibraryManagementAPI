"""Module containing statistics service abstractions."""
from abc import ABC, abstractmethod
from typing import List

from src.core.domain.statistics import TopBorrowedBooks, MonthlyBorrowedBooks, YearSummary, MonthlyCategoryStats


class IStatisticsService(ABC):
    """A class representing statistics service abstractions."""
    @abstractmethod
    async def get_top_borrowed_books(self) -> List[TopBorrowedBooks]:
        """The method getting the top borrowed books.

        Returns:
            List[TopBorrowedBooks]: A list of top borrowed books.
        """

    @abstractmethod
    async def get_monthly_borrowed_books(self) -> List[MonthlyBorrowedBooks]:
        """The method getting the list of books borrowed monthly.

        Returns:
            List[MonthlyBorrowedBooks]: A list of books borrowed monthly.
        """

    @abstractmethod
    async def get_year_summary(self, year: int) -> YearSummary:
        """The method getting a summary of borrowed books for the given year.

        Args:
            year (int): The year to get the summary for.

        Returns:
            The summary data for the specified year.
        """

    @abstractmethod
    async def get_average_borrowed_per_category_monthly(self) -> List[MonthlyCategoryStats]:
        """The method getting the average number of books borrowed per category each month.

        Returns:
            The average number of borrows per category for each month.
        """