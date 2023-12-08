from fastapi import APIRouter
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse
from decimal import Decimal
from app.db.base import get_session
from app.db.queries import products as queries
from app.api.responses import CONFLICT

from app.models.products import (
    ProductInsertModel, ProductListModel,
    ProductResponseModel
)

router = APIRouter()


@router.get("/product", response_model=ProductListModel)
async def get_products(
    price: Decimal,
    session: AsyncSession=Depends(get_session)
):
    """
    Get the list of products whose cost does not exceed the specified price
    """
    try:
        products = await queries.get_products(session, price)
        return {'detail': 'success', 'products': products}
    except IntegrityError as _:
        detail = 'database error'
        return JSONResponse({'detail': 'error', 'message': detail},
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@router.post("/product", status_code=status.HTTP_201_CREATED,
             response_model=ProductResponseModel, responses=CONFLICT)
async def add_product(
    product: ProductInsertModel,
    session: AsyncSession=Depends(get_session)
):
    """
    Create product
    """
    try:
        new_product = await queries.add_product(session, product)
    except IntegrityError as _:
        detail = 'product with that name already exists in company'
        return JSONResponse({'detail': 'error', 'message': detail},
                            status_code=status.HTTP_409_CONFLICT)
    try:
        await session.commit()
        return {'detail': 'success', 'product': new_product}
    except IntegrityError as _:
        detail = f'product was not added due to database error'
        return JSONResponse({'detail': 'error', 'message': detail}, 
                             status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
