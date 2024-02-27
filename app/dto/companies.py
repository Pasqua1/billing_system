from pydantic import BaseModel, ConfigDict

from app.usecase.utils.responses import ResponseModel


class CompanyBaseModel(BaseModel):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


class CompanyInsertModel(BaseModel):
    company_name: str


class CompanyFullModel(CompanyBaseModel, CompanyInsertModel):
    pass


class CompanyResponseModel(ResponseModel):
    company: CompanyFullModel


class CompanyListModel(ResponseModel):
    companies: list[CompanyFullModel]
