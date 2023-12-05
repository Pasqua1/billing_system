from fastapi import APIRouter
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse
from db.base import get_session
from db.queries import currency_types as queries

from models.currency_types import (
    CurrencyTypeModel, CurrencyTypeListModel,
    CurrencyTypeResponseModel
)

router = APIRouter()


@router.get("/currency_types", response_model=CurrencyTypeListModel)
async def get_currency_types(session: AsyncSession=Depends(get_session)):
    """
    Get the list of available currency types
    """
    currency_types = await queries.get_currency_types(session)
    return {'detail': 'success', 'currency_types': currency_types}


@router.post("/currency_types", response_model=CurrencyTypeResponseModel)
async def add_currency_type(
    currency_type: CurrencyTypeModel,
    session: AsyncSession=Depends(get_session)
):
    """
    Create currency type
    """
    new_currency_type = await queries.add_currency_type(session, currency_type)
    try:
        await session.commit()
        return {'detail': 'success', 'currency_type': new_currency_type}
    except IntegrityError as _:
        detail = f'currency type was not added due to database conflict'
        return JSONResponse({'detail': 'error', 'message': detail}, 
                             status_code=status.HTTP_409_CONFLICT)

