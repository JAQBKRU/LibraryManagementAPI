"""Main module of the app"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator


from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler


from src.api.routers.user import router as user_router
from src.api.routers.book import router as book_router
from src.api.routers.lend import router as lend_router
from src.api.routers.publisher import router as publisher_router
from src.api.routers.statistic import router as statistics_router

from src.container import Container
from src.db import database
from src.db import init_db

from src.init_data import init_data

container = Container()
container.wire(modules=[
    "src.api.routers.user",
    "src.api.routers.book",
    "src.api.routers.lend",
    "src.api.routers.publisher",
    "src.api.routers.statistic",
])

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    await init_data()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/user")
app.include_router(book_router, prefix="/book")
app.include_router(lend_router, prefix="/lend")
app.include_router(publisher_router, prefix="/publisher")
app.include_router(statistics_router, prefix="/statistics")

@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:
    """A function handling http exceptions for logging purposes.

    Args:
        request (Request): The incoming HTTP request.
        exception (HTTPException): A related exception.

    Returns:
        Response: The HTTP response.
    """
    return await http_exception_handler(request, exception)