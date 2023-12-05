from fastapi import APIRouter
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse
from db.base import get_session
from db.queries import transaction_statuses as queries

from models.transaction_statuses import (
    TransactionStatusModel, TransactionStatusListModel,
    TransactionStatusResponseModel
)

router = APIRouter()


@router.get("/transaction_statuses", response_model=TransactionStatusListModel)
async def get_transaction_statuses(session: AsyncSession=Depends(get_session)):
    """
    Get the list of available transaction statuses
    """
    transaction_statuses = await queries.get_transaction_statuses(session)
    return {'detail': 'success', 'transaction_statuses': transaction_statuses}


@router.post("/transaction_statuses", response_model=TransactionStatusResponseModel)
async def add_transaction_status(
    transaction_status: TransactionStatusModel,
    session: AsyncSession=Depends(get_session)
):
    """
    Create transaction status
    """
    new_status = await queries.add_transaction_status(session, transaction_status)
    try:
        await session.commit()
        return {'detail': 'success', 'transaction_status': new_status}
    except IntegrityError as _:
        detail = f'status was not added due to database conflict'
        return JSONResponse({'detail': 'error', 'message': detail}, 
                             status_code=status.HTTP_409_CONFLICT)

