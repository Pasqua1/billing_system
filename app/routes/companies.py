from fastapi import APIRouter
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse
from app.service.database import get_session
from app.service.queries import companies as queries
from app.usecase.utils.response import HTTP_409_CONFLICT

from app.dto.companies import (
    CompanyInsertModel, CompanyListModel,
    CompanyResponseModel
)

router = APIRouter()


@router.get("/companies", response_model=CompanyListModel)
async def get_companies(session: AsyncSession = Depends(get_session)):
    """
    Get the list of available companies
    """
    companies = await queries.get_companies(session)
    return {'detail': 'success', 'companies': companies}


@router.post("/companies", status_code=status.HTTP_201_CREATED,
             response_model=CompanyResponseModel, responses=HTTP_409_CONFLICT)
async def add_company(
        company: CompanyInsertModel,
        session: AsyncSession = Depends(get_session)
):
    """
    Create company
    """
    new_company = await queries.add_company(session, company)
    await session.commit()
    return {'detail': 'success', 'company': new_company}
