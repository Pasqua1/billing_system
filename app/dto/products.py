import typing
from pydantic import BaseModel
from decimal import Decimal

from app.usecase.utils.responses import ResponseModel


class ProductBaseModel(BaseModel):
    product_id: int


class ProductAttributeModel(BaseModel):
    product_name: str
    price: Decimal
    quantity: int


class ProductInsertModel(ProductAttributeModel):
    company_id: int
    currency_type_id: int


class ProductFullInsertModel(ProductBaseModel, ProductInsertModel):
    pass


class ProductFullModel(ProductBaseModel, ProductAttributeModel):
    company_name: str
    currency_type_name: str


class ProductResponseModel(ResponseModel):
    product: typing.Optional[ProductFullModel | ProductFullInsertModel]


class ProductListModel(ResponseModel):
    products: list[ProductFullModel]
