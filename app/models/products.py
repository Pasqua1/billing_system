import typing
from pydantic import BaseModel
from decimal import Decimal
from sqlalchemy import Column, String, Integer, Numeric, ForeignKey
from app.db.base import Base

from app.models import ResponseModel


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String)
    company_id = Column(Integer, ForeignKey("companies.company_id"))
    price = Column(Numeric)
    quantity = Column(Integer)
    currency_type_id = Column(Integer, ForeignKey("currency_types.currency_type_id"))


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


class ProductFullModel(ProductBaseModel,ProductAttributeModel):
    company_name: str
    currency_type_name: str


class ProductResponseModel(ResponseModel):
    product: typing.Optional[ProductFullModel|ProductFullInsertModel]


class ProductListModel(ResponseModel):
    products: list[ProductFullModel]
