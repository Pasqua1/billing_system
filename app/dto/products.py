from pydantic import BaseModel, ConfigDict
from decimal import Decimal

from app.usecase.utils.responses import ResponseModel


class ProductBaseModel(BaseModel):
    product_id: int
    model_config = ConfigDict(from_attributes=True)


class ProductAttributeModel(BaseModel):
    product_name: str
    price: Decimal
    quantity: int


class ProductInsertModel(ProductAttributeModel):
    company_id: int
    currency_type_id: int


class ProductFullModel(ProductBaseModel, ProductInsertModel):
    pass


class ProductResponseModel(ResponseModel):
    product: ProductFullModel


class ProductListModel(ResponseModel):
    products: list[ProductFullModel]
