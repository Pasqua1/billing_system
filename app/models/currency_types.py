import typing
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer
from db.base import Base

from models import ResponseModel


class CurrencyType(Base):
    __tablename__ = "currency_types"

    currency_type_id = Column(Integer, primary_key=True, autoincrement=True)
    currency_type_name = Column(String)


class CurrencyTypeModel(BaseModel):
    currency_type_id: int
    currency_type_name: str


class CurrencyTypeResponseModel(ResponseModel):
    currency_type: typing.Optional[CurrencyTypeModel]


class CurrencyTypeListModel(ResponseModel):
    currency_types: list[CurrencyTypeModel]
