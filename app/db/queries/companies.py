from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from models.companies import Company, CompanyModel


async def get_companies(session: AsyncSession) -> list[CompanyModel]:
    result = await session.execute(select(Company))
    companies = result.scalars().all()
    companies = [
        CompanyModel(company_id=company.company_id,
                     company_name=company.company_name) for company in companies
    ]
    return companies


async def add_company(session: AsyncSession, company: CompanyModel) -> Company:
    result = await session.execute(insert(Company).
                                 values(company_name=company.company_name).
                                 returning(Company))
    return result.scalar()
