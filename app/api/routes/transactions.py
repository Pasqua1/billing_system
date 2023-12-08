from fastapi import APIRouter
from fastapi import Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse
from app.db.base import get_session
from app.db.queries import transactions as queries
from app.db.queries import customers as customers_queries
from app.db.queries import products as products_queries
from app.api.responses import CONFLICT, NOT_FOUND

from app.models.transactions import (
    TransactionInsertModel, TransactionListModel,
    TransactionResponseModel
)

router = APIRouter()


@router.get("/transaction", response_model=TransactionResponseModel,
            responses=NOT_FOUND)
async def get_transaction_by_transaction_id(
    transaction_id: int,
    session: AsyncSession=Depends(get_session)
):
    """
    Get transaction
    """
    try:
        transaction = await queries.get_transaction_by_transaction_id(session, transaction_id)
        return {'detail': 'success', 'transaction': transaction}
    except IntegrityError as _:
        detail = 'database error'
        return JSONResponse({'detail': 'error', 'message': detail},
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@router.get("/transactions/customer", response_model=TransactionListModel)
async def get_transactions_of_customer(
    customer_id: int,
    session: AsyncSession=Depends(get_session)
):
    """
    Get transactions of customer
    """
    try:
        transactions = await queries.get_transactions_of_customer(session, customer_id)
        return {'detail': 'success', 'transactions': transactions}
    except IntegrityError as _:
        detail = 'database error'
        return JSONResponse({'detail': 'error', 'message': detail},
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE)



@router.get("/transactions", response_model=TransactionListModel)
async def get_transaction_in_range(
    amount: int,
    session: AsyncSession=Depends(get_session)
):
    """
    Get transactions in range of amount
    """
    try:
        transactions = await queries.get_transactions_in_range(session, amount)
        return {'detail': 'success', 'transactions': transactions}
    except IntegrityError as _:
        detail = 'database error'
        return JSONResponse({'detail': 'error', 'message': detail},
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@router.post("/payment", status_code=status.HTTP_201_CREATED,
             response_model=TransactionResponseModel, responses=(CONFLICT | NOT_FOUND))
async def add_payment(
    payment: TransactionInsertModel,
    session: AsyncSession=Depends(get_session)
):
    """
    Create payment
    """
    try:
        customer = await customers_queries.get_customer(session, payment.customer_id)
        product = await products_queries.get_product(session, payment.product_id)
        if customer.currency_type_name != product.currency_type_name:
            detail=f'currecy type of customer doesn\'t match with product currecny type'
            return JSONResponse({'detail': 'error', 'message': detail},
                            status_code=status.HTTP_409_CONFLICT)
        new_balance = customer.balance - payment.amount
        await customers_queries.update_customer_balance(session, payment.customer_id, new_balance)
        new_quantity = product.quantity - payment.number_of_products
        await products_queries.update_product_quantity(session, payment.product_id, new_quantity)
        new_payment = await queries.add_payment(session, payment)
    except IntegrityError as _:
        detail = 'payment was not added due to database conflict'
        return JSONResponse({'detail': 'error', 'message': detail},
                            status_code=status.HTTP_409_CONFLICT)
    try:
        await session.commit()
        return {'detail': 'success', 'transaction': new_payment}
    except IntegrityError as _:
        detail = f'payment was not added due to database error'
        return JSONResponse({'detail': 'error', 'message': detail}, 
                             status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    