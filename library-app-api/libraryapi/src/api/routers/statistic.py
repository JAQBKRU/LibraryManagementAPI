"""A module containing statistics endpoints."""
from typing import List

from dependency_injector.wiring import inject, Provide
from fastapi import Depends, APIRouter, HTTPException

from src.container import Container
from src.core.domain.statistics import Statistics, MonthlyBorrowedBooks, YearSummary, MonthlyCategoryStats

from src.infrastructure.services.istatistics import IStatisticsService

router = APIRouter()

@router.get("/top_10_borrowed_books", tags=["Statistics"], response_model=Statistics, status_code=200)
@inject
async def get_top10_borrowed_books(
        service: IStatisticsService = Depends(Provide[Container.statistics_service]),
    ) -> Statistics:
    """An endpoint for retrieving the top 10 most borrowed books.

    Args:
        service (IStatisticsService, optional): The injected service dependency.

    Raises:
        HTTPException:
            - 404 if no data is available for the top borrowed books.

    Returns:
        Statistics: The top 10 most borrowed books.
    """
    top_books = await service.get_top_borrowed_books()
    if not top_books:
        raise HTTPException(status_code=404, detail="No data")

    return Statistics(top_books=top_books)

@router.get("/monthly_borrowed_books", tags=["Statistics"], response_model=List[MonthlyBorrowedBooks], status_code=200)
@inject
async def get_monthly_borrowed_books(
        service: IStatisticsService = Depends(Provide[Container.statistics_service]),
) -> List[MonthlyBorrowedBooks]:
    """An endpoint for retrieving monthly statistics of borrowed books.

    Args:
        service (IStatisticsService, optional): The injected service dependency.

    Raises:
        HTTPException:
            - 404 if no data is available for the monthly borrowed books.

    Returns:
        List[MonthlyBorrowedBooks]: A list of monthly borrowed book statistics.
    """
    monthly_books = await service.get_monthly_borrowed_books()
    if not monthly_books:
        raise HTTPException(status_code=404, detail="No data")

    return monthly_books

@router.get("/yearly_summary/{year}", tags=["Statistics"], response_model=YearSummary, status_code=200)
@inject
async def get_year_summary(
        year: int,
        service: IStatisticsService = Depends(Provide[Container.statistics_service]),
) -> YearSummary:
    """An endpoint for retrieving a yearly summary of borrowed books for a given year.

    Args:
        year (int): The year for which the summary is to be fetched.
        service (IStatisticsService, optional): The injected service dependency.

    Raises:
        HTTPException:
            - 404 if no data is available for the requested year.

    Returns:
        YearSummary: The summary of borrowed books for the requested year.
    """
    year_summary = await service.get_year_summary(year)
    if not year_summary:
        raise HTTPException(status_code=404, detail="No data")

    return year_summary

@router.get("/average_borrowed_per_category_monthly", tags=["Statistics"], response_model=List[MonthlyCategoryStats], status_code=200)
@inject
async def get_average_borrowed_per_category_monthly(
        service: IStatisticsService = Depends(Provide[Container.statistics_service]),
) -> List[MonthlyCategoryStats]:
    """An endpoint for retrieving the average number of borrowed books per category monthly.

    Returns:
        List[MonthlyCategoryStats]: A list of statistics with the average number of books borrowed per category each month.

    Raises:
        HTTPException:
            - 404 if no data is available.
    """
    average_borrowed = await service.get_average_borrowed_per_category_monthly()
    if not average_borrowed:
        raise HTTPException(status_code=404, detail="No data available")

    return average_borrowed