from sqlalchemy import select
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.transaction_statuses import (
    TransactionStatusFullModel,
    TransactionStatusInsertModel
)
from app.entity.transaction_statuses import TransactionStatus


async def get_transaction_status_by_status_name(
        session: AsyncSession,
        status_name: str
) -> TransactionStatusFullModel:
    result = await session.scalars(
        select(TransactionStatus).where(TransactionStatus.status_name == status_name))
    transaction_statuses = [
        TransactionStatusFullModel.model_validate(
            transaction_status) for transaction_status in result
    ]
    if not transaction_statuses:
        raise HTTPException(detail=f"status with status_name={status_name} not found",
                            status_code=status.HTTP_404_NOT_FOUND)
    return TransactionStatusFullModel.model_validate(transaction_statuses[0])


async def get_transaction_statuses(session: AsyncSession) -> list[TransactionStatusFullModel]:
    result = await session.scalars(select(TransactionStatus))
    transaction_statuses = [
        TransactionStatusFullModel.model_validate(
            transaction_status) for transaction_status in result
    ]
    return transaction_statuses


async def add_transaction_status(
        session: AsyncSession,
        transaction_status: TransactionStatusInsertModel
) -> TransactionStatus:
    new_transaction_status = TransactionStatus(**transaction_status.model_dump())
    session.add(new_transaction_status)
    await session.commit()
    await session.refresh(new_transaction_status)
    return new_transaction_status
