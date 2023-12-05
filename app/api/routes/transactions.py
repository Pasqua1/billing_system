from fastapi import APIRouter
from fastapi import Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse
from db.base import get_session
from db.queries import transactions as queries
from db.queries.customers import update_customer_balance
from db.queries.products import update_product_quantity

from models.transactions import (
    TransactionModel, TransactionListModel,
    TransactionResponseModel
)

router = APIRouter()


@router.get("/transaction/{transaction_id}", response_model=TransactionResponseModel)
async def get_transaction_by_transaction_id(
    transaction_id: int = Path(alias='transaction_id'),
    session: AsyncSession=Depends(get_session)
):
    """
    Get transaction
    """
    transaction = await queries.get_transaction_by_transaction_id(session, transaction_id)
    return {'detail': 'success', 'transaction': transaction}


@router.get("/transactions/{customer_id}", response_model=TransactionListModel)
async def get_transaction_of_customer(
    customer_id: int = Path(alias='customer_id'),
    session: AsyncSession=Depends(get_session)
):
    """
    Get transactions of customer
    """
    transactions = await queries.get_transaction_of_customer(session, customer_id)
    return {'detail': 'success', 'transactions': transactions}


@router.get("/transactions/", response_model=TransactionListModel)
async def get_transaction_in_range(
    amount: int,
    session: AsyncSession=Depends(get_session)
):
    """
    Get transactions in range of amount
    """
    transactions = await queries.get_transaction_in_range(session, amount)
    return {'detail': 'success', 'transactions': transactions}


@router.post("/payment", response_model=TransactionResponseModel)
async def add_payment(
    payment: TransactionModel,
    session: AsyncSession=Depends(get_session)
):
    """
    Create payment
    """
    await update_customer_balance(session, payment.customer_id, payment.number_of_products)
    await update_product_quantity(session, payment.product_id, payment.amount)
    new_payment = await queries.add_payment(session, payment)
    try:
        await session.commit()
        return {'detail': 'success', 'transaction': new_payment}
    except IntegrityError as _:
        detail = f'payment was not added due to database conflict'
        return JSONResponse({'detail': 'error', 'message': detail}, 
                             status_code=status.HTTP_409_CONFLICT)
    