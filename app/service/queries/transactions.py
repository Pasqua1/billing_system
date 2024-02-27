from sqlalchemy import select
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.entity.customers import Customer
from app.entity.transactions import Transaction
from app.dto.transactions import (
    TransactionInsertModel,
    TransactionFullModel
)


async def get_transaction_by_transaction_id(
        session: AsyncSession,
        transaction_id: int
) -> TransactionFullModel:
    transaction = await session.get(Customer, transaction_id)
    if transaction is None:
        raise HTTPException(detail=f"transaction with id={transaction_id} not found",
                            status_code=status.HTTP_404_NOT_FOUND)
    return TransactionFullModel.model_validate(transaction)


async def get_transactions_of_customer(
        session: AsyncSession,
        customer_id: int
) -> list[TransactionFullModel]:
    result = await session.scalars(select(Transaction).
                                   where(Transaction.customer_id == customer_id))
    transactions = [
        TransactionFullModel.model_validate(transaction) for transaction in result
    ]
    return transactions


async def get_transactions_in_range(
        session: AsyncSession,
        amount: int
) -> list[TransactionFullModel]:
    result = await session.scalars(select(Transaction).
                                   where(Transaction.amount <= amount))
    transactions = [
        TransactionFullModel.model_validate(transaction) for transaction in result
    ]
    return transactions


async def add_payment(
        session: AsyncSession,
        transaction: TransactionInsertModel
) -> Transaction:
    new_transaction = Transaction(**transaction.model_dump())
    session.add(new_transaction)
    await session.commit()
    await session.refresh(new_transaction)
    return new_transaction
