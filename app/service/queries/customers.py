from decimal import Decimal
from sqlalchemy import select, update
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.entity.customers import Customer
from app.dto.customers import CustomerInsertModel, CustomerFullInsertModel


async def get_customer(session: AsyncSession,
                       customer_id: int) -> CustomerFullInsertModel:
    customer = await session.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(detail=f'customer with id={customer_id} not found',
                            status_code=status.HTTP_404_NOT_FOUND)
    return CustomerFullInsertModel.model_validate(customer)


async def update_customer_balance(session: AsyncSession,
                                  customer_id: int,
                                  new_balance: Decimal) -> Customer:
    customer = await session.scalar(update(Customer).
                                    where(Customer.customer_id == customer_id).
                                    values(balance=new_balance).
                                    returning(Customer))
    return customer


async def get_company_customers(session: AsyncSession,
                                company_id: int) -> list[CustomerFullInsertModel]:
    result = await session.scalars(select(Customer).
                                   where(Customer.company_id == company_id))
    customers = [
        CustomerFullInsertModel.model_validate(customer) for customer in result
    ]
    return customers


async def add_customer(session: AsyncSession,
                       customer: CustomerInsertModel) -> Customer:
    new_customer = Customer(**customer.model_dump())
    session.add(new_customer)
    await session.commit()
    await session.refresh(new_customer)
    return new_customer
