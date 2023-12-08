import typing
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer
from app.db.base import Base

from app.models import ResponseModel


class CurrencyType(Base):
    __tablename__ = "currency_types"

    currency_type_id = Column(Integer, primary_key=True, autoincrement=True)
    currency_type_name = Column(String)


class CurrencyTypeBaseModel(BaseModel):
    currency_type_id: int


class CurrencyTypeInsertModel(BaseModel):
    currency_type_name: str


class CurrencyTypeFullModel(CurrencyTypeBaseModel, CurrencyTypeInsertModel):
    pass


class CurrencyTypeResponseModel(ResponseModel):
    currency_type: typing.Optional[CurrencyTypeFullModel]


class CurrencyTypeListModel(ResponseModel):
    currency_types: list[CurrencyTypeFullModel]
