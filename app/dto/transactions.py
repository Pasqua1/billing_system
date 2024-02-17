import typing
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from sqlalchemy import Column, Integer, Numeric, ForeignKey, TIMESTAMP
from app.service.database import Base

from app.usecase.utils.responses import ResponseModel


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    date_create = Column(TIMESTAMP, default=datetime.now())
    amount = Column(Numeric, nullable=False)
    status_id = Column(Integer, ForeignKey("transaction_statuses.status_id"))
    currency_type_id = Column(Integer, ForeignKey("currency_types.currency_type_id"))
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    number_of_products = Column(Integer)


class TransactionBaseModel(BaseModel):
    transaction_id: int
    date_create: datetime


class TransactionAttributeModel(BaseModel):
    amount: Decimal
    number_of_products: int


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
