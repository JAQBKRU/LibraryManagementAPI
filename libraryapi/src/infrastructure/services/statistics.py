"""Module containing statistics service implementation."""
from typing import List

from src.core.domain.statistics import TopBorrowedBooks, MonthlyBorrowedBooks, MonthlyCategoryStats
from src.core.repositories.istatistics import IStatisticsRepository
from src.infrastructure.services.istatistics import IStatisticsService

class StatisticsService(IStatisticsService):
    """A class implementing the statistics service."""
    _repository: IStatisticsRepository

    def __init__(self, repository: IStatisticsRepository) -> None:
        """The initializer of the `statistics service`.

        Args:
            repository (IStatisticsRepository): The reference to the statistics repository.
        """
        self._repository = repository

    async def get_top_borrowed_books(self) -> List[TopBorrowedBooks]:
        """The method getting the top borrowed books.

        Returns:
            List[TopBorrowedBooks]: The list of the top borrowed books.
        """
        return await self._repository.get_top_borrowed_books()

    async def get_monthly_borrowed_books(self) -> List[MonthlyBorrowedBooks]:
        """The method getting the monthly borrowed books.

        Returns:
            List[MonthlyBorrowedBooks]: The list of the monthly borrowed books.
        """
        return await self._repository.get_monthly_borrowed_books()

    async def get_year_summary(self, year: int):
        """The method getting the yearly statistics summary.

        Args:
            year (int): The year for which the summary is requested.

        Returns:
            Any: The yearly summary data.
        """
        return await self._repository.get_year_summary(year)

    async def get_average_borrowed_per_category_monthly(self) -> List[MonthlyCategoryStats]:
        """The method getting the average number of books borrowed per category each month.

        Returns:
            List[MonthlyCategoryStats]: A list of average number of books borrowed per category each month.
        """
        return await self._repository.get_average_borrowed_per_category_monthly()
