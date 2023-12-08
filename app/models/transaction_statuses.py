import typing
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer
from app.db.base import Base

from app.models import ResponseModel


class TransactionStatus(Base):
    __tablename__ = "transaction_statuses"

    status_id = Column(Integer, primary_key=True, autoincrement=True)
    status_name = Column(String)


class TransactionStatusBaseModel(BaseModel):
    status_id: int


class TransactionStatusInsertModel(BaseModel):
    status_name: str


class TransactionStatusFullModel(TransactionStatusBaseModel, TransactionStatusInsertModel):
    pass


class TransactionStatusResponseModel(ResponseModel):
    transaction_status: typing.Optional[TransactionStatusFullModel]


class TransactionStatusListModel(ResponseModel):
    transaction_statuses: list[TransactionStatusFullModel]
