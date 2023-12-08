from fastapi import APIRouter
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse
from app.db.base import get_session
from app.db.queries import companies as queries
from app.api.responses import CONFLICT

from app.models.companies import (
    CompanyInsertModel, CompanyListModel,
    CompanyResponseModel
)

router = APIRouter()


@router.get("/companies", response_model=CompanyListModel)
async def get_companies(session: AsyncSession=Depends(get_session)):
    """
    Get the list of available companies
    """
    try:
        companies = await queries.get_companies(session)
        return {'detail': 'success', 'companies': companies}
    except IntegrityError as _:
        detail = 'database error'
        return JSONResponse({'detail': 'error', 'message': detail},
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@router.post("/companies", status_code=status.HTTP_201_CREATED,
             response_model=CompanyResponseModel, responses=CONFLICT)
async def add_company(
    company: CompanyInsertModel,
    session: AsyncSession=Depends(get_session)
):
    """
    Create company
    """
    try:
        new_company = await queries.add_company(session, company)
    except IntegrityError as _:
        detail = 'company with thit name already exists'
        return JSONResponse({'detail': 'error', 'message': detail},
                            status_code=status.HTTP_409_CONFLICT)
    try:
        await session.commit()
        return {'detail': 'success', 'company': new_company}
    except IntegrityError as _:
        detail = 'company was not added due to database error'
        return JSONResponse({'detail': 'error', 'message': detail}, 
                             status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
