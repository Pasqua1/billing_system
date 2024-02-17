import typing
from enum import Enum

from pydantic import BaseModel, Field


class Detail(str, Enum):
    success = 'success'
    error = 'error'
    timeout = 'timeout'


class ResponseModel(BaseModel):
    detail: Detail
    message: typing.Optional[typing.Any] = Field(None, description='optional error description')
