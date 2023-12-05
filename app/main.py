from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from api.errors import database_exception_handler, http_exception_handler, http422_error_handler
from api.routes.api import router
from api.responses import SERVICE_UNAVAILABLE


def make_app() -> FastAPI:

    app = FastAPI(
        responses=SERVICE_UNAVAILABLE
    )
    app.add_middleware(
        CORSMiddleware,
        allow_headers=['*'],
        expose_headers=['*'],
        allow_methods=['*'],
        allow_credentials=False
    )
    app.add_exception_handler(Exception, database_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, http422_error_handler)
    app.include_router(router)

    return app

app = make_app()
