import typing
from pydantic import BaseModel, ConfigDict

from app.usecase.utils.responses import ResponseModel


class CurrencyTypeBaseModel(BaseModel):
    currency_type_id: int


class CurrencyTypeInsertModel(BaseModel):
    currency_type_name: str


class CurrencyTypeFullModel(CurrencyTypeBaseModel, CurrencyTypeInsertModel):
    model_config = ConfigDict(from_attributes=True)


class CurrencyTypeResponseModel(ResponseModel):
    currency_type: typing.Optional[CurrencyTypeFullModel]


class CurrencyTypeListModel(ResponseModel):
    currency_types: list[CurrencyTypeFullModel]
