from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime

from app.usecase.utils.responses import ResponseModel


class TransactionBaseModel(BaseModel):
    transaction_id: int


class TransactionAttributeModel(BaseModel):
    status_id: int = 1
    amount: Decimal = 0
    currency_type_id: int = 0
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class TransactionInsertModel(BaseModel):
    quantity: int
    customer_id: int
    product_id: int
    model_config = ConfigDict(from_attributes=True)


class TransactionFullInsertModel(TransactionInsertModel, TransactionAttributeModel):
    pass


class TransactionFullModel(TransactionAttributeModel, TransactionInsertModel):
    pass


class TransactionResponseModel(ResponseModel):
    transaction: TransactionFullModel


class TransactionListModel(ResponseModel):
    transactions: list[TransactionFullModel]
