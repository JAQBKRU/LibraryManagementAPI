"""Module providing containers injecting dependencies."""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from src.infrastructure.repositories.lenddb import LendRepository
from src.infrastructure.repositories.publisherdb import PublisherRepository
from src.infrastructure.repositories.userdb import UserRepository
from src.infrastructure.repositories.bookdb import BookRepository
from src.infrastructure.repositories.statisticsdb import StatisticsRepository
from src.infrastructure.services.lend import LendService
from src.infrastructure.services.publisher import PublisherService
from src.infrastructure.services.statistics import StatisticsService

from src.infrastructure.services.user import UserService
from src.infrastructure.services.book import BookService


class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    user_repository = Singleton(UserRepository)
    book_repository = Singleton(BookRepository)
    lend_repository = Singleton(LendRepository)
    publisher_repository = Singleton(PublisherRepository)
    statistics_repository = Singleton(StatisticsRepository)

    user_service = Factory(
        UserService,
        repository=user_repository,
    )

    book_service = Factory(
        BookService,
        repository=book_repository,
    )

    lend_service = Factory(
        LendService,
        repository=lend_repository,
        book_service=book_service,
        user_service=user_service,
    )

    publisher_service = Factory(
        PublisherService,
        repository=publisher_repository,
    )

    statistics_service = Factory(
        StatisticsService,
        repository=statistics_repository,
    )