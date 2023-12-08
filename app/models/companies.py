import typing
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer
from app.db.base import Base

from app.models import ResponseModel


class Company(Base):
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String)


class CompanyBaseModel(BaseModel):
    company_id: int


class CompanyInsertModel(BaseModel):
    company_name: str


class CompanyFullModel(CompanyBaseModel,CompanyInsertModel):
    pass


class CompanyResponseModel(ResponseModel):
    company: typing.Optional[CompanyFullModel]
    

class CompanyListModel(ResponseModel):
    companies: list[CompanyFullModel]
