from fastapi import APIRouter
from fastapi import Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse
from app.service.database import get_session
from app.service.queries import transactions as queries
from app.service.queries import customers as customers_queries
from app.service.queries import products as products_queries
from app.usecase.utils.response import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND

from app.dto.transactions import (
    TransactionInsertModel, TransactionListModel,
    TransactionResponseModel
)

router = APIRouter()


@router.get("/transactions", response_model=TransactionResponseModel,
            responses=HTTP_404_NOT_FOUND)
async def get_transaction_by_transaction_id(
        transaction_id: int,
        session: AsyncSession = Depends(get_session)
):
    """
    Get transaction
    """
    transaction = await queries.get_transaction_by_transaction_id(session, transaction_id)
    return {'detail': 'success', 'transaction': transaction}


@router.get("/transactions/customer", response_model=TransactionListModel)
async def get_transactions_of_customer(
        customer_id: int,
        session: AsyncSession = Depends(get_session)
):
    """
    Get transactions of customer
    """

    transactions = await queries.get_transactions_of_customer(session, customer_id)
    return {'detail': 'success', 'transactions': transactions}


@router.get("/transactions", response_model=TransactionListModel)
async def get_transaction_in_range(
        amount: int,
        session: AsyncSession = Depends(get_session)
):
    """
    Get transactions in range of amount
    """

    transactions = await queries.get_transactions_in_range(session, amount)
    return {'detail': 'success', 'transactions': transactions}


@router.post("/payment", status_code=status.HTTP_201_CREATED,
             response_model=TransactionResponseModel, responses=(HTTP_409_CONFLICT | HTTP_404_NOT_FOUND))
async def add_payment(
        payment: TransactionInsertModel,
        session: AsyncSession = Depends(get_session)
):
    """
    Create payment
    """
    customer = await customers_queries.get_customer(session, payment.customer_id)
    product = await products_queries.get_product(session, payment.product_id)

    if customer.currency_type_name != product.currency_type_name:
        detail = f'currecy type of customer doesn\'t match with product currecny type'
        return JSONResponse({'detail': 'error', 'message': detail},
                            status_code=status.HTTP_409_CONFLICT)

    new_balance = customer.balance - payment.amount
    await customers_queries.update_customer_balance(session, payment.customer_id, new_balance)

    new_quantity = product.quantity - payment.number_of_products
    await products_queries.update_product_quantity(session, payment.product_id, new_quantity)

    new_payment = await queries.add_payment(session, payment)

    await session.commit()
    return {'detail': 'success', 'transaction': new_payment}
