import typing
from pydantic import BaseModel
from decimal import Decimal

from app.usecase.utils.responses import ResponseModel


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
    customer: typing.Optional[CustomerFullModel | CustomerFullInsertModel]


class CustomerListModel(ResponseModel):
    customers: list[CustomerFullModel]
