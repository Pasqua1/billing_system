from sqlalchemy import select, insert, update
from fastapi import HTTPException, status
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from app.entity.companies import Company
from app.entity.currency_types import CurrencyType
from app.entity.customers import Customer
from app.dto.customers import CustomerInsertModel, CustomerFullModel


async def get_customer(session: AsyncSession, customer_id: int) -> CustomerFullModel:
    result = await session.execute(select(Customer, Company, CurrencyType).
                                   where(Customer.customer_id == customer_id).
                                   join(Company).
                                   join(CurrencyType))
    customer = None
    for row in result:
        customer = CustomerFullModel(
            customer_id=row.Customer.customer_id,
            customer_name=row.Customer.customer_name,
            company_name=row.Company.company_name,
            balance=row.Customer.balance,
            currency_type_name=row.CurrencyType.currency_type_name
        )
    if customer is None:
        raise HTTPException(detail=f'customer with id={customer_id} not found',
                            status_code=status.HTTP_404_NOT_FOUND)
    return customer


async def update_customer_balance(session: AsyncSession,
                                  customer_id: int,
                                  new_balance: Decimal) -> Customer:
    result = await session.execute(update(Customer).
                                   where(Customer.customer_id == customer_id).
                                   values(balance=new_balance).
                                   returning(Customer))
    return result.scalar()


async def get_company_customers(session: AsyncSession,
                                company_id: int) -> list[CustomerFullModel]:
    result = await session.execute(select(Customer, Company, CurrencyType).
                                   where(Customer.company_id == company_id).
                                   join(Company).
                                   join(CurrencyType))
    customers = []
    for row in result:
        customer = CustomerFullModel(
            customer_id=row.Customer.customer_id,
            customer_name=row.Customer.customer_name,
            company_name=row.Company.company_name,
            balance=row.Customer.balance,
            currency_type_name=row.CurrencyType.currency_type_name
        )
        customers.append(customer)
    return customers


async def add_customer(session: AsyncSession, customer: CustomerInsertModel) -> Customer:
    result = await session.execute(insert(Customer).
                                   values(customer_name=customer.customer_name,
                                          company_id=customer.company_id,
                                          balance=customer.balance,
                                          currency_type_id=customer.currency_type_id).
                                   returning(Customer))
    return result.scalar()
