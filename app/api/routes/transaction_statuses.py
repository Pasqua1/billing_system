from fastapi import APIRouter
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse
from app.db.base import get_session
from app.db.queries import transaction_statuses as queries
from app.api.responses import CONFLICT

from app.models.transaction_statuses import (
    TransactionStatusInsertModel, TransactionStatusListModel,
    TransactionStatusResponseModel
)

router = APIRouter()


@router.get("/transaction_statuses", response_model=TransactionStatusListModel)
async def get_transaction_statuses(session: AsyncSession=Depends(get_session)):
    """
    Get the list of available transaction statuses
    """
    try:
        transaction_statuses = await queries.get_transaction_statuses(session)
        return {'detail': 'success', 'transaction_statuses': transaction_statuses}
    except IntegrityError as _:
        detail = 'database error'
        return JSONResponse({'detail': 'error', 'message': detail},
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@router.post("/transaction_statuses", status_code=status.HTTP_201_CREATED,
             response_model=TransactionStatusResponseModel, responses=CONFLICT)
async def add_transaction_status(
    transaction_status: TransactionStatusInsertModel,
    session: AsyncSession=Depends(get_session)
):
    """
    Create transaction status
    """
    try:
        new_status = await queries.add_transaction_status(session, transaction_status)
    except IntegrityError as _:
        detail = 'status with that name already exists'
        return JSONResponse({'detail': 'error', 'message': detail},
                            status_code=status.HTTP_409_CONFLICT)
    try:
        await session.commit()
        return {'detail': 'success', 'transaction_status': new_status}
    except IntegrityError as _:
        detail = f'status was not added due to database error'
        return JSONResponse({'detail': 'error', 'message': detail}, 
                             status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

