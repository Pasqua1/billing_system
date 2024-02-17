from fastapi import APIRouter
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse
from app.service.database import get_session
from app.service.queries import currency_types as queries
from app.usecase.utils.response import HTTP_409_CONFLICT

from app.dto.currency_types import (
    CurrencyTypeInsertModel, CurrencyTypeListModel,
    CurrencyTypeResponseModel
)

router = APIRouter()


@router.get("/currency_types", response_model=CurrencyTypeListModel)
async def get_currency_types(session: AsyncSession = Depends(get_session)):
    """
    Get the list of available currency types
    """
    currency_types = await queries.get_currency_types(session)
    return {'detail': 'success', 'currency_types': currency_types}


@router.post("/currency_types", status_code=status.HTTP_201_CREATED,
             response_model=CurrencyTypeResponseModel, responses=HTTP_409_CONFLICT)
async def add_currency_type(
    currency_type: CurrencyTypeInsertModel,
    session: AsyncSession = Depends(get_session)
):
    """
    Create currency type
    """
    new_currency_type = await queries.add_currency_type(session, currency_type)
    await session.commit()
    return {'detail': 'success', 'currency_type': new_currency_type}

