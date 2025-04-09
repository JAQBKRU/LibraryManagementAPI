"""Module containing statistics repository implementation."""
from typing import List

from fastapi import HTTPException
from sqlalchemy import select, func, join

from src.core.domain.lend import LendStatus
from src.core.repositories.istatistics import IStatisticsRepository
from src.core.domain.statistics import TopBorrowedBooks, MonthlyBorrowedBooks, YearSummary, MonthlyCategoryStats
from src.db import (
    book_table,
    lend_table,
    database,
)

class StatisticsRepository(IStatisticsRepository):
    """Repository class for handling statistics-related operations."""
    async def get_top_borrowed_books(self) -> List[TopBorrowedBooks]:
        """Fetch the top 10 most borrowed books.

        Returns:
            List[TopBorrowedBooks]: A list of the top 10 most borrowed books.
        """
        query = (
            select(
                book_table.c.id,
                book_table.c.title,
                func.count(lend_table.c.id).label("borrow_count")
            )
            .select_from(
                book_table.join(lend_table, book_table.c.id == lend_table.c.book_id)
            )
            .group_by(book_table.c.id, book_table.c.title)
            .order_by(func.count(lend_table.c.id).desc())
            .limit(10)
        )

        rows = await database.fetch_all(query)
        return [
            TopBorrowedBooks(
                id=row["id"],
                title=row["title"],
                borrow_count=row["borrow_count"])
            for row in rows
        ]

    async def get_monthly_borrowed_books(self) -> List[MonthlyBorrowedBooks]:
        """Fetch the number of books borrowed each month.

        Returns:
            List[MonthlyBorrowedBooks]: A list of books borrowed per month.
        """
        month_name_expr = func.trim(func.to_char(lend_table.c.borrowed_date, 'Month')).label("month")

        query = (
            select(
                month_name_expr,
                func.count(lend_table.c.id).label("borrow_count_per_month")
            )
            .group_by(month_name_expr)
            .order_by(func.count(lend_table.c.id).desc())
        )

        rows = await database.fetch_all(query)
        return [
            MonthlyBorrowedBooks(
                month=row["month"],
                borrow_count=row["borrow_count_per_month"])
            for row in rows
        ]

    async def get_year_summary(self, year: int) -> YearSummary:
        """Fetch the borrowing summary for a specific year, including
        the total number of borrows and the most borrowed book.

        Args:
            year (int): The year for which the summary is to be fetched.

        Returns:
            YearSummary: A summary of borrows for the given year, including the total
            borrows and the most borrowed book.

        Raises:
            HTTPException: If no data is found for the given year.
        """
        year_expr = func.extract('year', lend_table.c.borrowed_date).label("year")

        query = (
            select(
                year_expr,
                func.count(lend_table.c.id).label("total_borrows"),

                (select(lend_table.c.book_id)
                 .where(func.extract('year', lend_table.c.borrowed_date) == year)
                 .where(
                    (lend_table.c.status == LendStatus.borrowed.value) |
                    (lend_table.c.status == LendStatus.returned.value)
                )
                 .group_by(lend_table.c.book_id)
                 .order_by(func.count(lend_table.c.book_id).desc())
                 .limit(1)
                 ).scalar_subquery().label("most_borrowed_book_id"),

                (select(book_table.c.title)
                 .where(book_table.c.id ==
                        (select(lend_table.c.book_id)
                         .where(func.extract('year', lend_table.c.borrowed_date) == year)
                         .where(
                            (lend_table.c.status == LendStatus.borrowed.value) |
                            (lend_table.c.status == LendStatus.returned.value)
                        )
                         .group_by(lend_table.c.book_id)
                         .order_by(func.count(lend_table.c.book_id).desc())
                         .limit(1)
                         )
                        )
                 ).scalar_subquery().label("most_borrowed_book_title")
            )
            .where(func.extract('year', lend_table.c.borrowed_date) == year)
            .where(
                (lend_table.c.status == LendStatus.borrowed.value) |
                (lend_table.c.status == LendStatus.returned.value)
            )
            .group_by(year_expr)
        )

        rows = await database.fetch_all(query)
        if not rows:
            raise HTTPException(status_code=404, detail=f"No data for year {year}")

        return YearSummary(
            year=year,
            total_borrows=rows[0]["total_borrows"],
            most_borrowed_book_title=rows[0]["most_borrowed_book_title"],
        )

    async def get_average_borrowed_per_category_monthly(self) -> List[MonthlyCategoryStats]:
        """Fetch the average number of books borrowed per category each month.

        Returns:
            List[MonthlyCategoryStats]: A list of monthly statistics per category, including average borrows per month.
        """
        month_expr = func.to_char(lend_table.c.borrowed_date, 'YYYY-MM').label("month")
        query = (
            select(
                month_expr,
                book_table.c.categories,
                (func.count(lend_table.c.id) / func.count(func.distinct(lend_table.c.borrowed_date))).label("average_borrow_count")
            )
            .select_from(
                join(lend_table, book_table, lend_table.c.book_id == book_table.c.id)
            )
            .group_by(month_expr, book_table.c.categories)
            .order_by(month_expr.desc())
        )

        rows = await database.fetch_all(query)

        return [
            MonthlyCategoryStats(
                month=row["month"],
                category=row["categories"],
                average_borrows_per_month=row["average_borrow_count"]
            )
            for row in rows
        ]