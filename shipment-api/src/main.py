"""Main module for the FastAPI application."""

from contextlib import asynccontextmanager
from sys import modules
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers.seed import router as seed_router
from src.api.routers.shipment import router as shipment_router
from src.api.routers.staff import router as staff_router
from src.api.routers.user import router as user_router
from src.container import Container
from src.db import database, init_db

container = Container()
container.wire(
    modules=[
        "src.api.routers.shipment",
        "src.api.routers.user",
        "src.core.security.auth",
        "src.api.routers.seed",
        "src.api.routers.staff",
    ]
)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(shipment_router)
app.include_router(user_router)
app.include_router(seed_router)
app.include_router(staff_router)


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:
    return await http_exception_handler(request, exception)
