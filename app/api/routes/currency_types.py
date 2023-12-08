from fastapi import APIRouter
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse
from app.db.base import get_session
from app.db.queries import currency_types as queries
from app.api.responses import CONFLICT

from app.models.currency_types import (
    CurrencyTypeInsertModel, CurrencyTypeListModel,
    CurrencyTypeResponseModel
)

router = APIRouter()


@router.get("/currency_types", response_model=CurrencyTypeListModel)
async def get_currency_types(session: AsyncSession=Depends(get_session)):
    """
    Get the list of available currency types
    """
    try:
        currency_types = await queries.get_currency_types(session)
        return {'detail': 'success', 'currency_types': currency_types}
    except IntegrityError as _:
        detail = 'database error'
        return JSONResponse({'detail': 'error', 'message': detail},
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@router.post("/currency_types", status_code=status.HTTP_201_CREATED,
             response_model=CurrencyTypeResponseModel, responses=CONFLICT)
async def add_currency_type(
    currency_type: CurrencyTypeInsertModel,
    session: AsyncSession=Depends(get_session)
):
    """
    Create currency type
    """
    try:
        new_currency_type = await queries.add_currency_type(session, currency_type)
    except IntegrityError as _:
        detail = 'currency type with that name already exists'
        return JSONResponse({'detail': 'error', 'message': detail},
                            status_code=status.HTTP_409_CONFLICT)
    try:
        await session.commit()
        return {'detail': 'success', 'currency_type': new_currency_type}
    except IntegrityError as _:
        detail = 'currency type was not added due to database error'
        return JSONResponse({'detail': 'error', 'message': detail}, 
                             status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

