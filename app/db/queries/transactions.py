from sqlalchemy import select, insert
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transactions import Transaction, TransactionInsertModel, TransactionFullModel
from app.models.products import Product
from app.models.customers import Customer
from app.models.transaction_statuses import TransactionStatus
from app.models.currency_types import CurrencyType


async def get_transaction_by_transaction_id(session: AsyncSession, transaction_id: int) -> Transaction:
    result = await session.execute(
        select(Transaction,
                TransactionStatus,
                CurrencyType,
                Product,
                Customer).
        where(Transaction.transaction_id==transaction_id).
        where(Transaction.status_id == TransactionStatus.status_id).
        where(Transaction.currency_type_id == CurrencyType.currency_type_id).
        where(Transaction.product_id == Product.product_id).
        where(Transaction.customer_id == Customer.customer_id)
    )
    transaction = None
    for row in result:
        transaction = TransactionFullModel(
            transaction_id=row.Transaction.transaction_id,
            date_create=row.Transaction.date_create,
            amount=row.Transaction.amount,
            status_name=row.TransactionStatus.status_name,
            currency_type_name=row.CurrencyType.currency_type_name,
            customer_name=row.Customer.customer_name,
            product_name=row.Product.product_name,
            number_of_products=row.Transaction.number_of_products
        )
    if transaction is None:
        raise HTTPException(detail=f'transaction with id={transaction_id} not found',
                            status_code=status.HTTP_404_NOT_FOUND)
    return transaction


async def get_transactions_of_customer(session: AsyncSession, customer_id: int) -> list[TransactionFullModel]:
    result = await session.execute(
        select(Transaction,
                TransactionStatus,
                CurrencyType,
                Product,
                Customer).
        where(Transaction.customer_id == customer_id).
        where(Transaction.status_id == TransactionStatus.status_id).
        where(Transaction.currency_type_id == CurrencyType.currency_type_id).
        where(Transaction.product_id == Product.product_id).
        where(Transaction.customer_id == Customer.customer_id))
    transactions = []
    for row in result:
        transaction = TransactionFullModel(
            transaction_id=row.Transaction.transaction_id,
            date_create=row.Transaction.date_create,
            amount=row.Transaction.amount,
            status_name=row.TransactionStatus.status_name,
            currency_type_name=row.CurrencyType.currency_type_name,
            customer_name=row.Customer.customer_name,
            product_name=row.Product.product_name,
            number_of_products=row.Transaction.number_of_products
        )
        transactions.append(transaction)
    return transactions


async def get_transactions_in_range(session: AsyncSession, amount: int) -> list[TransactionFullModel]:
    result = await session.execute(
        select(Transaction,
                TransactionStatus,
                CurrencyType,
                Product,
                Customer).
        where(Transaction.amount<=amount).
        where(Transaction.status_id == TransactionStatus.status_id).
        where(Transaction.currency_type_id == CurrencyType.currency_type_id).
        where(Transaction.product_id == Product.product_id).
        where(Transaction.customer_id == Customer.customer_id))
    transactions = []
    for row in result:
        transaction = TransactionFullModel(
            transaction_id=row.Transaction.transaction_id,
            date_create=row.Transaction.date_create,
            amount=row.Transaction.amount,
            status_name=row.TransactionStatus.status_name,
            currency_type_name=row.CurrencyType.currency_type_name,
            customer_name=row.Customer.customer_name,
            product_name=row.Product.product_name,
            number_of_products=row.Transaction.number_of_products
        )
        transactions.append(transaction)
    return transactions

async def add_payment(session: AsyncSession, transaction: TransactionInsertModel) -> Transaction:
    result = await session.execute(insert(Transaction).
                                 values(amount=transaction.amount,
                                        status_id=transaction.status_id,
                                        currency_type_id=transaction.currency_type_id,
                                        customer_id=transaction.customer_id,
                                        product_id=transaction.product_id,
                                        number_of_products=transaction.number_of_products).
                                 returning(Transaction))
    return result.scalar()