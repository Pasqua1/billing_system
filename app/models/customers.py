import typing
from pydantic import BaseModel
from decimal import Decimal
from sqlalchemy import Column, String, Integer, Numeric, ForeignKey
from db.base import Base

from models import ResponseModel


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String)
    company_id = Column(Integer, ForeignKey("companies.company_id"))
    balance = Column(Numeric)
    currency_type_id = Column(Integer, ForeignKey("currency_types.currency_type_id"))


class CustomerModel(BaseModel):
    customer_id: int
    customer_name: str
    company_id: int
    balance: Decimal
    currency_type_id: int


class CustomerResponseModel(ResponseModel):
    customer: typing.Optional[CustomerModel]


class CustomerListModel(ResponseModel):
    customers: list[CustomerModel]
