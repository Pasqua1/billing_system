from fastapi import APIRouter
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse
from app.service.database import get_session
from app.service.queries import transaction_statuses as queries
from app.usecase.utils.response import HTTP_409_CONFLICT

from app.dto.transaction_statuses import (
    TransactionStatusInsertModel, TransactionStatusListModel,
    TransactionStatusResponseModel
)

router = APIRouter()


@router.get("/transaction_statuses", response_model=TransactionStatusListModel)
async def get_transaction_statuses(
        session: AsyncSession = Depends(get_session)
):
    """
    Get the list of available transaction statuses
    """
    transaction_statuses = await queries.get_transaction_statuses(session)
    return {'detail': 'success', 'transaction_statuses': transaction_statuses}


@router.post("/transaction_statuses", status_code=status.HTTP_201_CREATED,
             response_model=TransactionStatusResponseModel, responses=HTTP_409_CONFLICT)
async def add_transaction_status(
        transaction_status: TransactionStatusInsertModel,
        session: AsyncSession = Depends(get_session)
):
    """
    Create transaction status
    """
    new_status = await queries.add_transaction_status(session, transaction_status)
    return {'detail': 'success', 'transaction_status': new_status}
