import typing
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer
from db.base import Base

from models import ResponseModel


class Company(Base):
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String)


class CompanyModel(BaseModel):
    company_id: int
    company_name: str


class CompanyResponseModel(ResponseModel):
    company: typing.Optional[CompanyModel]
    

class CompanyListModel(ResponseModel):
    companies: list[CompanyModel]
