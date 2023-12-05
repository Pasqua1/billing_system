from sqlalchemy import select, insert, update
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from models.customers import Customer, CustomerModel
from models.companies import Company
from models.currency_types import CurrencyType


async def get_customer(session: AsyncSession, customer_id: int) -> CustomerModel:
    result = await session.execute(select(Customer, Company, CurrencyType).
                                   where(Customer.customer_id==customer_id).
                                   join(Company).
                                   join(CurrencyType))
    for row in result:
        customer = CustomerModel(
            customer_id=row.Customer.customer_id,
            customer_name=row.Customer.customer_name,
            company_name=row.Company.company_name,
            balance=row.Customer.balance,
            currency_type_name=row.CurrencyType.currency_type_name
        )
    return customer


async def update_customer_balance(session: AsyncSession, 
                                 customer_id: int, 
                                 amount: Decimal) -> Customer:
    customer = await get_customer(session, customer_id)
    if customer:
        new_balance = customer.balance - amount
        result = await session.execute(update(Customer).
                                    where(Customer.customer_id==customer_id).
                                    values(balance=new_balance).
                                    returning(Customer))
        return result.scalar()
    return None
        


async def get_company_customers(session: AsyncSession,
                                company_id: int) -> list[CustomerModel]:
    result = await session.execute(select(Customer, Company, CurrencyType).
                                   where(Customer.company_id==company_id).
                                   join(Company).
                                   join(CurrencyType))
    customers = []
    for row in result:
        customer = CustomerModel(
            customer_id=row.Customer.customer_id,
            customer_name=row.Customer.customer_name,
            company_name=row.Company.company_name,
            balance=row.Customer.balance,
            currency_type_name=row.CurrencyType.currency_type_name
        )
        customers.append(customer)
    return customers


async def add_customer(session: AsyncSession, customer: CustomerModel) -> Customer:
    result = await session.execute(insert(Customer).
                                   values(customer_name=customer.customer_name,
                                          company_id=customer.company_id,
                                          balance=customer.balance,
                                          currency_type_id=customer.currency_type_id).
                                   returning(Customer))
    return result.scalar()