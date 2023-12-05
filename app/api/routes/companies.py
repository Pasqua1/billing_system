from fastapi import APIRouter
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse
from db.base import get_session
from db.queries import companies as queries

from models.companies import (
    CompanyModel, CompanyListModel,
    CompanyResponseModel
)

router = APIRouter()


@router.get("/companies", response_model=CompanyListModel)
async def get_companies(session: AsyncSession=Depends(get_session)):
    """
    Get the list of available companies
    """
    companies = await queries.get_companies(session)
    return {'detail': 'success', 'companies': companies}


@router.post("/companies", response_model=CompanyResponseModel)
async def add_company(
    company: CompanyModel,
    session: AsyncSession=Depends(get_session)
):
    """
    Create company
    """
    new_company = await queries.add_company(session, company)
    try:
        await session.commit()
        return {'detail': 'success', 'company': new_company}
    except IntegrityError as _:
        detail = f'company was not added due to database conflict'
        return JSONResponse({'detail': 'error', 'message': detail}, 
                             status_code=status.HTTP_409_CONFLICT)
