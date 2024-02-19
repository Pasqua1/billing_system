from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.currency_types import CurrencyTypeFullModel, CurrencyTypeInsertModel
from app.entity.currency_types import CurrencyType


async def get_currency_types(session: AsyncSession) -> list[CurrencyTypeFullModel]:
    result = await session.scalars(select(CurrencyType))
    currency_types = [
        CurrencyTypeFullModel.model_validate(
            currency_type) for currency_type in result
    ]
    return currency_types


async def add_currency_type(session: AsyncSession,
                            currency_type: CurrencyTypeInsertModel) -> CurrencyType:
    new_currency_type = CurrencyType(**currency_type.model_dump())
    session.add(new_currency_type)
    await session.commit()
    await session.refresh(new_currency_type)
    return new_currency_type
