import contextlib
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import DBAPIError
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

from app.usecase.utils.exception_handler import (
    database_error_handler,
    unprocessable_entity_handler,
    http_exception_handler
)
from app.routes.router import router
from app.usecase.utils.response import HTTP_503_SERVICE_UNAVAILABLE


def make_app() -> FastAPI:

    app = FastAPI(
        title=settings.NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        responses=HTTP_503_SERVICE_UNAVAILABLE
    )
    app.add_middleware(
        CORSMiddleware,
        allow_headers=['*'],
        expose_headers=['*'],
        allow_methods=['*'],
        allow_credentials=False
    )
    app.add_exception_handler(DBAPIError, database_error_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, unprocessable_entity_handler)
    app.include_router(router)

    return app


app = make_app()
