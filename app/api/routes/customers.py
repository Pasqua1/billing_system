from fastapi import APIRouter
from fastapi import Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse
from db.base import get_session
from db.queries import customers as queries

from models.customers import (
    CustomerModel, CustomerListModel,
    CustomerResponseModel
)

router = APIRouter()


@router.get("/customer/{customer_id}", response_model=CustomerResponseModel)
async def get_customer(
    customer_id: int = Path(alias='customer_id'),
    session: AsyncSession=Depends(get_session)
):
    """
    Get customer
    """
    customer = await queries.get_customer(session, customer_id)
    return {'detail': 'success', 'customer': customer}


@router.patch("/customer/{customer_id}/{balance}", response_model=CustomerResponseModel)
async def update_balance(
    customer_id: int = Path(alias='customer_id'),
    amount: int = Path(alias='balance'),
    session: AsyncSession=Depends(get_session)
):
    """
    Reduces the customer's balance by the amount
    """
    customer = await queries.update_customer_balance(session, customer_id, amount)
    try:
        await session.commit()
        return {'detail': 'success', 'customer': customer}
    except IntegrityError as e:
        detail = f'customer was not added due to database conflict'
        return JSONResponse({'detail': 'error', 'message': detail}, 
                             status_code=status.HTTP_409_CONFLICT)


@router.get("/customer/company/{company_id}", response_model=CustomerListModel)
async def get_company_customers(
    company_id: int = Path(alias='company_id'),
    session: AsyncSession=Depends(get_session)
):
    """
    Get the customers of the company
    """
    customers = await queries.get_company_customers(session, company_id)
    return {'detail': 'success', 'customers': customers}


@router.post("/customer", response_model=CustomerResponseModel)
async def add_customer(
    customer: CustomerModel,
    session: AsyncSession=Depends(get_session)
):
    """
    Create customer
    """
    new_customer = await queries.add_customer(session, customer)
    try:
        await session.commit()
        return {'detail': 'success', 'customer': new_customer}
    except IntegrityError as e:
        detail = f'customer was not added due to database conflict'
        return JSONResponse({'detail': 'error', 'message': detail}, 
                             status_code=status.HTTP_409_CONFLICT)
