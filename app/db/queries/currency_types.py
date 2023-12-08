from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.currency_types import CurrencyType, CurrencyTypeFullModel, CurrencyTypeInsertModel


async def get_currency_types(session: AsyncSession) -> list[CurrencyTypeFullModel]:
    result = await session.execute(select(CurrencyType))
    currency_types = result.scalars().all()
    currency_types = [
        CurrencyTypeFullModel(
            currency_type_id=currency_type.currency_type_id,
            currency_type_name=currency_type.currency_type_name
        ) for currency_type in currency_types
    ]
    return currency_types

async def add_currency_type(session: AsyncSession,
                            currency_type: CurrencyTypeInsertModel) -> CurrencyType:
    result = await session.execute(insert(CurrencyType).
                                   values(currency_type_name=currency_type.currency_type_name).
                                   returning(CurrencyType))
    return result.scalar()