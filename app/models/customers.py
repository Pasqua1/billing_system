import typing
from pydantic import BaseModel
from decimal import Decimal
from sqlalchemy import Column, String, Integer, Numeric, ForeignKey
from app.db.base import Base

from app.models import ResponseModel


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String)
    company_id = Column(Integer, ForeignKey("companies.company_id"))
    balance = Column(Numeric)
    currency_type_id = Column(Integer, ForeignKey("currency_types.currency_type_id"))


class CustomerBaseModel(BaseModel):
    customer_id: int


class CustomerAttributeModel(BaseModel):
    customer_name: str
    balance: Decimal


class CustomerInsertModel(CustomerAttributeModel):
    company_id: int
    currency_type_id: int


class CustomerFullInsertModel(CustomerBaseModel, CustomerInsertModel):
    pass


class CustomerFullModel(CustomerBaseModel, CustomerAttributeModel):
    company_name: str
    currency_type_name: str


class CustomerResponseModel(ResponseModel):
    customer: typing.Optional[CustomerFullModel|CustomerFullInsertModel]


class CustomerListModel(ResponseModel):
    customers: list[CustomerFullModel]
