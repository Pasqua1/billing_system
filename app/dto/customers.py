from pydantic import BaseModel, ConfigDict
from decimal import Decimal

from app.usecase.utils.responses import ResponseModel


class CustomerBaseModel(BaseModel):
    customer_id: int
    model_config = ConfigDict(from_attributes=True)


class CustomerAttributeModel(BaseModel):
    customer_name: str
    balance: Decimal


class CustomerInsertModel(CustomerAttributeModel):
    company_id: int
    currency_type_id: int


class CustomerFullInsertModel(CustomerBaseModel, CustomerInsertModel):
    pass


class CustomerResponseModel(ResponseModel):
    customer: CustomerFullInsertModel


class CustomerListModel(ResponseModel):
    customers: list[CustomerFullInsertModel]
