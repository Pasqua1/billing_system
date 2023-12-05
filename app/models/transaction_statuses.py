import typing
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer
from db.base import Base

from models import ResponseModel


class TransactionStatus(Base):
    __tablename__ = "transaction_statuses"

    status_id = Column(Integer, primary_key=True, autoincrement=True)
    status_name = Column(String)


class TransactionStatusModel(BaseModel):
    status_id: int
    status_name: str


class TransactionStatusResponseModel(ResponseModel):
    transaction_status: typing.Optional[TransactionStatusModel]


class TransactionStatusListModel(ResponseModel):
    transaction_statuses: list[TransactionStatusModel]
