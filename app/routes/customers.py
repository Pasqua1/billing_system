from fastapi import APIRouter
from fastapi import Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse
from app.service.database import get_session
from app.service.queries import customers as queries
from app.usecase.utils.response import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND

from app.dto.customers import (
    CustomerListModel,
    CustomerResponseModel, CustomerInsertModel
)

router = APIRouter()


@router.get("/customer", response_model=CustomerResponseModel,
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


@router.patch("/customer", status_code=200,
              response_model=CustomerResponseModel, responses=HTTP_404_NOT_FOUND)
async def update_balance(
        customer_id: int,
        amount: int,
        session: AsyncSession = Depends(get_session)
):
    """
    Reduces the customer's balance by the amount
    """
    customer = await queries.get_customer(session, customer_id)
    new_balance = customer.balance - amount
    customer = await queries.update_customer_balance(session, customer_id,
                                                     new_balance)
    await session.commit()
    return {'detail': 'success', 'customer': customer}


@router.get("/customer/company", response_model=CustomerListModel)
async def get_company_customers(
        company_id: int,
        session: AsyncSession = Depends(get_session)
):
    """
    Get the customers of the company
    """
    customers = await queries.get_company_customers(session, company_id)
    return {'detail': 'success', 'customers': customers}


@router.post("/customer", status_code=status.HTTP_201_CREATED,
             response_model=CustomerResponseModel, responses=HTTP_409_CONFLICT)
async def add_customer(
        customer: CustomerInsertModel,
        session: AsyncSession = Depends(get_session)
):
    """
    Create customer
    """

    new_customer = await queries.add_customer(session, customer)
    await session.commit()
    return {'detail': 'success', 'customer': new_customer}
