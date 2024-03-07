from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.companies import CompanyFullModel, CompanyInsertModel
from app.entity.companies import Company


async def get_companies(session: AsyncSession) -> list[CompanyFullModel]:
    result = await session.scalars(select(Company))
    companies = [
        CompanyFullModel.model_validate(company) for company in result
    ]
    return companies


async def add_company(session: AsyncSession, company: CompanyInsertModel) -> Company:
    new_company = Company(**company.model_dump())
    session.add(new_company)
    await session.commit()
    await session.refresh(new_company)
    return new_company
