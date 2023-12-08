from fastapi import APIRouter
from fastapi import Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse
from app.db.base import get_session
from app.db.queries import customers as queries
from app.api.responses import CONFLICT, NOT_FOUND

from app.models.customers import (
    CustomerListModel,
    CustomerResponseModel,CustomerInsertModel
)

router = APIRouter()


@router.get("/customer", response_model=CustomerResponseModel,
            responses=NOT_FOUND)
async def get_customer(
    customer_id: int,
    session: AsyncSession=Depends(get_session)
):
    """
    Get customer
    """
    try:
        customer = await queries.get_customer(session, customer_id)
        return {'detail': 'success', 'customer': customer}
    except IntegrityError as _:
        detail = 'database error'
        return JSONResponse({'detail': 'error', 'message': detail},
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        

@router.patch("/customer", status_code=200,
              response_model=CustomerResponseModel, responses=NOT_FOUND)
async def update_balance(
    customer_id: int,
    amount: int,
    session: AsyncSession=Depends(get_session)
):
    """
    Reduces the customer's balance by the amount
    """
    try:
        customer = await queries.get_customer(session, customer_id)
        new_balance = customer.balance - amount
        customer = await queries.update_customer_balance(session, customer_id,
                                                         new_balance)
        await session.commit()
        return {'detail': 'success', 'customer': customer}
    except IntegrityError as _:
        detail = f'customer was not updated due to database error'
        return JSONResponse({'detail': 'error', 'message': detail}, 
                             status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@router.get("/customer/company", response_model=CustomerListModel)
async def get_company_customers(
    company_id: int,
    session: AsyncSession=Depends(get_session)
):
    """
    Get the customers of the company
    """
    try:
        customers = await queries.get_company_customers(session, company_id)
        return {'detail': 'success', 'customers': customers}
    except IntegrityError as _:
        detail = 'database error'
        return JSONResponse({'detail': 'error', 'message': detail},
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@router.post("/customer", status_code=status.HTTP_201_CREATED,
             response_model=CustomerResponseModel, responses=CONFLICT)
async def add_customer(
    customer: CustomerInsertModel,
    session: AsyncSession=Depends(get_session)
):
    """
    Create customer
    """
    try:
        new_customer = await queries.add_customer(session, customer)
    except IntegrityError as _:
        detail = 'customer was not added due to database conflict'
        return JSONResponse({'detail': 'error', 'message': detail},
                            status_code=status.HTTP_409_CONFLICT)
    try:
        await session.commit()
        return {'detail': 'success', 'customer': new_customer}
    except IntegrityError as _:
        detail = f'customer was not added due to database error'
        return JSONResponse({'detail': 'error', 'message': detail}, 
                             status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
