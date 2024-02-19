import typing
from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime

from app.usecase.utils.responses import ResponseModel


class TransactionBaseModel(BaseModel):
    transaction_id: int
    model_config = ConfigDict(from_attributes=True)


class TransactionAttributeModel(BaseModel):
    amount: Decimal
    quantity: int
    created_at: datetime
    updated_at: datetime


class TransactionInsertModel(TransactionAttributeModel):
    status_id: int
    currency_type_id: int
    customer_id: int
    product_id: int


class TransactionFullInsertModel(TransactionBaseModel, TransactionInsertModel):
    pass


class TransactionFullModel(TransactionBaseModel, TransactionAttributeModel):
    status_name: str
    currency_type_name: str
    customer_name: str
    product_name: str


class TransactionResponseModel(ResponseModel):
    transaction: typing.Optional[TransactionFullModel | TransactionFullInsertModel]


class TransactionListModel(ResponseModel):
    transactions: list[TransactionFullModel]
