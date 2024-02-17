from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.entity.companies import Company
from app.dto.companies import CompanyFullModel, CompanyInsertModel


async def get_companies(session: AsyncSession) -> list[CompanyFullModel]:
    result = await session.execute(select(Company))
    companies = result.scalars().all()
    companies = [
        CompanyFullModel(company_id=company.company_id,
                         company_name=company.company_name) for company in companies
    ]
    return companies


async def add_company(session: AsyncSession, company: CompanyInsertModel) -> Company:
    result = await session.execute(insert(Company).
                                   values(company_name=company.company_name).
                                   returning(Company))
    return result.scalar()
