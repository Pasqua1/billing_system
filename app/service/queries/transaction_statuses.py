from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.transaction_statuses import (
    TransactionStatusFullModel,
    TransactionStatusInsertModel
)
from app.entity.transaction_statuses import TransactionStatus


async def get_transaction_statuses(session: AsyncSession) -> list[TransactionStatusFullModel]:
    result = await session.scalars(select(TransactionStatus))
    currency_types = [
        TransactionStatusFullModel.model_validate(
            currency_type) for currency_type in result
    ]
    return currency_types


async def add_transaction_status(
        session: AsyncSession,
        transaction_status: TransactionStatusInsertModel
) -> TransactionStatus:
    new_transaction_status = TransactionStatus(**transaction_status.model_dump())
    session.add(new_transaction_status)
    await session.commit()
    await session.refresh(new_transaction_status)
    return new_transaction_status
