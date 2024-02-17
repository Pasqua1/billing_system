from typing import Union

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import DBAPIError


async def database_error_handler(
    _: Request, exc: DBAPIError,
) -> JSONResponse:
    detail = str(exc.orig).split('DETAIL:  ')[-1].rstrip('.')
    if "already exists" in detail:
        return JSONResponse(
            content={'successful': False, 'detail': detail},
            status_code=status.HTTP_409_CONFLICT,
        )
    return JSONResponse(
        content={'successful': False, 'detail': detail},
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    )


async def unprocessable_entity_handler(
        _: Request, exc: Union[RequestValidationError, ValidationError],
) -> JSONResponse:
    return JSONResponse(
        content={'successful': False, 'detail': str(exc)},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def http_exception_handler(
        _: Request, exc: HTTPException,
) -> JSONResponse:
    response = JSONResponse(
        content={'successful': False, 'detail': exc.detail},
        status_code=exc.status_code,
    )
    if exc.headers is not None:
        response.init_headers(exc.headers)

    return response
