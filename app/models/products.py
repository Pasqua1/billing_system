import typing
from pydantic import BaseModel
from decimal import Decimal
from sqlalchemy import Column, String, Integer, Numeric, ForeignKey
from db.base import Base

from models import ResponseModel


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String)
    price = Column(Numeric)
    quantity = Column(Integer)
    currency_type_id = Column(Integer, ForeignKey("currency_types.currency_type_id"))


class ProductModel(BaseModel):
    product_id: int
    product_name: str
    price: Decimal
    quantity: int
    currency_type_id: int


class ProductResponseModel(ResponseModel):
    product: typing.Optional[ProductModel]


class ProductListModel(ResponseModel):
    products: list[ProductModel]
