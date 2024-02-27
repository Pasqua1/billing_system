from pydantic import BaseModel, ConfigDict

from app.usecase.utils.responses import ResponseModel


class CurrencyTypeBaseModel(BaseModel):
    currency_type_id: int
    model_config = ConfigDict(from_attributes=True)


class CurrencyTypeInsertModel(BaseModel):
    currency_type_name: str


class CurrencyTypeFullModel(CurrencyTypeBaseModel, CurrencyTypeInsertModel):
    pass


class CurrencyTypeResponseModel(ResponseModel):
    currency_type: CurrencyTypeFullModel


class CurrencyTypeListModel(ResponseModel):
    currency_types: list[CurrencyTypeFullModel]
