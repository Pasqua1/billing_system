from datetime import datetime
from fastapi import APIRouter
from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.database import get_session
from app.service.queries import transactions as queries
from app.service.queries import customers as customers_queries
from app.service.queries import products as products_queries
from app.service.queries import transaction_statuses as transaction_statuses_queries
from app.usecase.utils.response import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND

from app.dto.transactions import (
    TransactionInsertModel, TransactionListModel,
    TransactionResponseModel, TransactionFullInsertModel
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


@router.get("/transactions/amount", response_model=TransactionListModel)
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
    status_name = 'NEW'
    try:
        transaction_status = await transaction_statuses_queries.get_transaction_status_by_status_name(
            session, status_name
        )
    except Exception as _:
        raise HTTPException(
            detail=f'There is no transaction_status with name = {status_name}',
            status_code=status.HTTP_404_NOT_FOUND
        )

    full_payment = TransactionFullInsertModel(**payment.model_dump())
    customer = await customers_queries.get_customer(session, payment.customer_id)
    product = await products_queries.get_product(session, payment.product_id)

    if customer.currency_type_id != product.currency_type_id:
        raise HTTPException(
            detail=f'currency_type of customer doesn\'t match with product currency_type',
            status_code=status.HTTP_409_CONFLICT
        )

    full_payment.currency_type_id = product.currency_type_id
    full_payment.amount = product.price * full_payment.quantity
    full_payment.status_id = transaction_status.status_id

    new_balance = customer.balance - full_payment.amount
    if new_balance < 0:
        raise HTTPException(
            detail=f'Not enough balance for customer with customer_id = {customer.customer_id}',
            status_code=status.HTTP_409_CONFLICT
        )
    await customers_queries.update_customer_balance(session, payment.customer_id, new_balance)

    new_quantity = product.quantity - full_payment.quantity
    if new_quantity < 0:
        raise HTTPException(
            detail=f'Not enough quantity for product with product_id = {product.product_id}',
            status_code=status.HTTP_409_CONFLICT
        )
    await products_queries.update_product_quantity(session, payment.product_id, new_quantity)

    full_payment.created_at = full_payment.updated_at = datetime.now()
    new_payment = await queries.add_payment(session, full_payment)

    return {'detail': 'success', 'transaction': new_payment}
