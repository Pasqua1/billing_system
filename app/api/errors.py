from typing import Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def database_exception_handler(_: Request, exception: HTTPException):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=jsonable_encoder({"detail": "error", 'message': str(exception)})
    )


async def http_exception_handler(_: Request, exception: HTTPException):
    return JSONResponse(
        status_code=exception.status_code,
        content={"detail": "error", "message": exception.detail}
    )


async def http422_error_handler(
    _: Request,
    exc: Union[RequestValidationError, ValidationError],
) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={'detail': 'error', "message": exc.errors()},
    )
