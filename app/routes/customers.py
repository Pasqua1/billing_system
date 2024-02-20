from decimal import Decimal
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.database import get_session
from app.service.queries import customers as queries
from app.usecase.utils.response import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND

from app.dto.customers import (
    CustomerListModel,
    CustomerResponseModel, CustomerInsertModel
)

router = APIRouter()


@router.get("/customers", response_model=CustomerResponseModel,
            responses=HTTP_404_NOT_FOUND)
async def get_customer(
        customer_id: int,
        session: AsyncSession = Depends(get_session)
):
    """
    Get customer
    """
    customer = await queries.get_customer(session, customer_id)
    return {'detail': 'success', 'customer': customer}


@router.patch("/customers", status_code=200,
              response_model=CustomerResponseModel,
              responses=(HTTP_404_NOT_FOUND | HTTP_409_CONFLICT))
async def update_balance(
        customer_id: int,
        new_balance: Decimal,
        session: AsyncSession = Depends(get_session)
):
    """
    Set the customer's new balance
    """
    if new_balance < 0:
        raise HTTPException(detail=f'new_balance should not be less than 0',
                            status_code=status.HTTP_409_CONFLICT)
    customer = await queries.update_customer_balance(session, customer_id,
                                                     new_balance)
    if customer is None:
        raise HTTPException(detail=f'customer with id={customer_id} not found',
                            status_code=status.HTTP_404_NOT_FOUND)
    await session.commit()
    await session.refresh(customer)
    return {'detail': 'success', 'customer': customer}


@router.get("/customers/company", response_model=CustomerListModel,
            responses=(HTTP_404_NOT_FOUND | HTTP_409_CONFLICT))
async def get_company_customers(
        company_id: int,
        session: AsyncSession = Depends(get_session)
):
    """
    Get the customers of the company
    """
    customers = await queries.get_company_customers(session, company_id)
    return {'detail': 'success', 'customers': customers}


@router.post("/customers", status_code=status.HTTP_201_CREATED,
             response_model=CustomerResponseModel, responses=HTTP_409_CONFLICT)
async def add_customer(
        customer: CustomerInsertModel,
        session: AsyncSession = Depends(get_session)
):
    """
    Create customer
    """
    if customer.balance < 0:
        raise HTTPException(detail=f'balance should not be less than 0',
                            status_code=status.HTTP_409_CONFLICT)
    new_customer = await queries.add_customer(session, customer)
    return {'detail': 'success', 'customer': new_customer}
