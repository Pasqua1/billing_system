import typing
from pydantic import BaseModel

from app.usecase.utils.responses import ResponseModel


class CompanyBaseModel(BaseModel):
    company_id: int


class CompanyInsertModel(BaseModel):
    company_name: str


class CompanyFullModel(CompanyBaseModel, CompanyInsertModel):
    pass


class CompanyResponseModel(ResponseModel):
    company: typing.Optional[CompanyFullModel]


class CompanyListModel(ResponseModel):
    companies: list[CompanyFullModel]
