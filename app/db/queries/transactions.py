from sqlalchemy import select, insert, outerjoin
from sqlalchemy.ext.asyncio import AsyncSession
from models.transactions import Transaction, TransactionModel
from models.products import Product
from models.customers import Customer
from models.transaction_statuses import TransactionStatus
from models.currency_types import CurrencyType


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
    for row in result:
        transaction = TransactionModel(
            transaction_id=row.Transaction.transaction_id,
            date_create=row.Transaction.date_create,
            amount=row.Transaction.amount,
            status_name=row.TransactionStatus.status_name,
            currency_type_name=row.CurrencyType.currency_type_name,
            customer_name=row.Customer.customer_name,
            product_name=row.Product.product_name,
            number_of_products=row.Transaction.number_of_products
        )
    return transaction


async def get_transaction_of_customer(session: AsyncSession, customer_id: int) -> list[TransactionModel]:
    result = await session.execute(
        select(Transaction,
                TransactionStatus,
                CurrencyType,
                Product,
                Customer).
        where(Transaction.customer_id==customer_id).
        where(Transaction.status_id == TransactionStatus.status_id).
        where(Transaction.currency_type_id == CurrencyType.currency_type_id).
        where(Transaction.product_id == Product.product_id).
        where(Transaction.customer_id == Customer.customer_id))
    transactions = []
    for row in result:
        transaction = TransactionModel(
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


async def get_transaction_in_range(session: AsyncSession, amount: int) -> list[TransactionModel]:
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
        transaction = TransactionModel(
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

async def add_payment(session: AsyncSession, transaction: TransactionModel) -> Transaction:
    result = await session.execute(insert(Transaction).
                                 values(amount=transaction.amount,
                                        status_id=transaction.status_id,
                                        currency_type_id=transaction.currency_type_id,
                                        customer_id=transaction.customer_id,
                                        product_id=transaction.product_id,
                                        number_of_products=transaction.number_of_products).
                                 returning(Transaction))
    return result.scalar()