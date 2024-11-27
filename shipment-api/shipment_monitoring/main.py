from contextlib import asynccontextmanager
from sys import modules
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from shipment_monitoring.api.routers.shipment import router as shipment_router
from shipment_monitoring.api.routers.user import router as user_router
from shipment_monitoring.container import Container
from shipment_monitoring.db import init_db, database


container = Container()
container.wire(
    modules=[
        "shipment_monitoring.api.routers.shipment",
        "shipment_monitoring.api.routers.user",
        "shipment_monitoring.api.utils.auth"
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
app.include_router(shipment_router)
app.include_router(user_router)



@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:
    return await http_exception_handler(request, exception)
