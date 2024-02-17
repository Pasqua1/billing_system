from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.entity.transaction_statuses import TransactionStatus
from app.dto.transaction_statuses import (
    TransactionStatusFullModel,
    TransactionStatusInsertModel
)


async def get_transaction_statuses(session: AsyncSession) -> list[TransactionStatusFullModel]:
    result = await session.execute(select(TransactionStatus))
    transaction_statuses = result.scalars().all()
    transaction_statuses = [
        TransactionStatusFullModel(
            status_id=status.status_id,
            status_name=status.status_name
        ) for status in transaction_statuses
    ]
    return transaction_statuses


async def add_transaction_status(
        session: AsyncSession,
        transaction_status: TransactionStatusInsertModel
) -> TransactionStatus:
    result = await session.execute(
        insert(TransactionStatus).
        values(status_name=transaction_status.status_name).
        returning(TransactionStatus)
    )
    return result.scalar()
