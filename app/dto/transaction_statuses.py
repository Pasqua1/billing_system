import typing
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, String, Integer
from app.service.database import Base

from app.usecase.utils.responses import ResponseModel


class TransactionStatusBaseModel(BaseModel):
    status_id: int
    model_config = ConfigDict(from_attributes=True)


class TransactionStatusInsertModel(BaseModel):
    status_name: str


class TransactionStatusFullModel(TransactionStatusBaseModel, TransactionStatusInsertModel):
    pass


class TransactionStatusResponseModel(ResponseModel):
    transaction_status: typing.Optional[TransactionStatusFullModel]


class TransactionStatusListModel(ResponseModel):
    transaction_statuses: list[TransactionStatusFullModel]
