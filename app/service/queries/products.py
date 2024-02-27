from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.entity.products import Product
from app.dto.products import ProductInsertModel, ProductFullModel


async def get_product(session: AsyncSession, product_id: int) -> ProductFullModel:
    product = await session.get(Product, product_id)
    if product is None:
        raise HTTPException(detail=f'product with id={product_id} not found',
                            status_code=status.HTTP_404_NOT_FOUND)
    return ProductFullModel.model_validate(product)


async def update_product_quantity(session: AsyncSession,
                                  product_id: int,
                                  new_quantity: int) -> Product:
    if new_quantity < 0:
        raise HTTPException(detail=f'new_quantity should not be less than 0',
                            status_code=status.HTTP_409_CONFLICT)
    product = await session.scalar(update(Product).
                                   where(Product.product_id == product_id).
                                   values(quantity=new_quantity).
                                   returning(Product))
    return product


async def get_products(session: AsyncSession, price: Decimal) -> list[ProductFullModel]:
    result = await session.scalars(select(Product).
                                   where(Product.price <= price))
    products = [
        ProductFullModel.model_validate(product) for product in result
    ]
    return products


async def add_product(session: AsyncSession, product: ProductInsertModel) -> Product:
    if product.price < 0:
        raise HTTPException(detail=f'price should not be less than 0',
                                   status_code=status.HTTP_409_CONFLICT)
    if product.quantity < 0:
        raise HTTPException(detail=f'quantity should not be less than 0',
                                   status_code=status.HTTP_409_CONFLICT)
    new_product = Product(**product.model_dump())
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return new_product
