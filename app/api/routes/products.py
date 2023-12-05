from fastapi import APIRouter
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse
from decimal import Decimal
from db.base import get_session
from db.queries import products as queries

from models.products import (
    ProductModel, ProductListModel,
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
    products = await queries.get_products(session, price)
    return {'detail': 'success', 'products': products}


@router.post("/product", response_model=ProductResponseModel)
async def add_product(
    product: ProductModel,
    session: AsyncSession=Depends(get_session)
):
    """
    Create product
    """
    new_product = await queries.add_product(session, product)
    try:
        await session.commit()
        return {'detail': 'success', 'product': new_product}
    except IntegrityError as _:
        detail = f'product was not added due to database conflict'
        return JSONResponse({'detail': 'error', 'message': detail}, 
                             status_code=status.HTTP_409_CONFLICT)
