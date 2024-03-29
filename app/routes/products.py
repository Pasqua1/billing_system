from fastapi import APIRouter
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
from app.service.database import get_session
from app.service.queries import products as queries
from app.usecase.utils.response import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from app.dto.products import (
    ProductInsertModel, ProductListModel,
    ProductResponseModel
)

router = APIRouter()


@router.get("/products", response_model=ProductResponseModel,
            responses=HTTP_404_NOT_FOUND)
async def get_customer(
        product_id: int,
        session: AsyncSession = Depends(get_session)
):
    """
    Get product
    """
    product = await queries.get_product(session, product_id)
    return {'detail': 'success', 'product': product}


@router.get("/products/price", response_model=ProductListModel)
async def get_products(
        price: Decimal,
        session: AsyncSession = Depends(get_session)
):
    """
    Get the list of products whose cost does not exceed the specified price
    """
    products = await queries.get_products(session, price)
    return {'detail': 'success', 'products': products}


@router.post("/products", status_code=status.HTTP_201_CREATED,
             response_model=ProductResponseModel, responses=HTTP_409_CONFLICT)
async def add_product(
        product: ProductInsertModel,
        session: AsyncSession = Depends(get_session)
):
    """
    Create product
    """
    new_product = await queries.add_product(session, product)
    return {'detail': 'success', 'product': new_product}
