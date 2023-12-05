from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from models.transactions import Transaction, TransactionModel


async def get_transaction_by_transaction_id(session: AsyncSession, transaction_id: int) -> Transaction:
    result = await session.execute(select(Transaction).
                                   where(Transaction.transaction_id==transaction_id))
    return result.scalar()


async def get_transaction_of_customer(session: AsyncSession, customer_id: int) -> list[TransactionModel]:
    result = await session.execute(select(Transaction).
                                   where(Transaction.customer_id==customer_id))
    transactions = result.scalars().all()
    transactions = [
        TransactionModel(
            transaction_id=transaction.transaction_id,
            date_create=transaction.date_create,
            amount=transaction.amount,
            status_id=transaction.status_id,
            currency_type_id=transaction.currency_type_id,
            customer_id=transaction.customer_id,
            product_id=transaction.product_id,
            number_of_products=transaction.number_of_products
        ) for transaction in transactions
    ]
    return transactions


async def get_transaction_in_range(session: AsyncSession, amount: int) -> list[TransactionModel]:
    result = await session.execute(select(Transaction).
                                   where(Transaction.amount<=amount))
    transactions = result.scalars().all()
    transactions = [
        TransactionModel(
            transaction_id=transaction.transaction_id,
            date_create=transaction.date_create,
            amount=transaction.amount,
            status_id=transaction.status_id,
            currency_type_id=transaction.currency_type_id,
            customer_id=transaction.customer_id,
            product_id=transaction.product_id,
            number_of_products=transaction.number_of_products
        ) for transaction in transactions
    ]
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