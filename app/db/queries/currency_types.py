from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from models.currency_types import CurrencyType, CurrencyTypeModel


async def get_currency_types(session: AsyncSession) -> list[CurrencyTypeModel]:
    result = await session.execute(select(CurrencyType))
    currency_types = result.scalars().all()
    currency_types = [
        CurrencyTypeModel(
            currency_type_id=currency_type.currency_type_id,
            currency_type_name=currency_type.currency_type_name
        ) for currency_type in currency_types
    ]
    return currency_types

async def add_currency_type(session: AsyncSession,
                            currency_type: CurrencyTypeModel) -> CurrencyType:
    result = await session.execute(insert(CurrencyType).
                                   values(currency_type_name=currency_type.currency_type_name).
                                   returning(CurrencyType))
    return result.scalar()