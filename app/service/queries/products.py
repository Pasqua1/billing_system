from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.entity.currency_types import CurrencyType
from app.entity.companies import Company
from app.entity.products import Product
from app.dto.products import ProductInsertModel, ProductFullModel


async def get_product(session: AsyncSession, product_id: int) -> ProductFullModel:
    result = await session.execute(select(Product, Company, CurrencyType).
                                   where(Product.product_id == product_id).
                                   join(Company).
                                   join(CurrencyType))
    product = None
    for row in result:
        product = ProductFullModel(
            product_id=row.Product.product_id,
            product_name=row.Product.product_name,
            price=row.Product.price,
            quantity=row.Product.quantity,
            company_name=row.Company.company_name,
            currency_type_name=row.CurrencyType.currency_type_name
        )
    if product is None:
        raise HTTPException(detail=f'product with id={product_id} not found',
                            status_code=status.HTTP_404_NOT_FOUND)
    return product


async def update_product_quantity(session: AsyncSession,
                                  product_id: int,
                                  new_quantity: int) -> Product:
    result = await session.execute(update(Product).
                                   where(Product.product_id == product_id).
                                   values(quantity=new_quantity).
                                   returning(Product))
    return result.scalar()


async def get_products(session: AsyncSession, price: Decimal) -> list[ProductFullModel]:
    result = await session.execute(select(Product, CurrencyType, Company).
                                   where(Product.price <= price).
                                   join(CurrencyType).
                                   join(Company))
    products = []
    for row in result:
        product = ProductFullModel(
            product_id=row.Product.product_id,
            product_name=row.Product.product_name,
            company_name=row.Company.company_name,
            price=row.Product.price,
            quantity=row.Product.quantity,
            currency_type_name=row.CurrencyType.currency_type_name
        )
        products.append(product)
    return products


async def add_product(session: AsyncSession, product: ProductInsertModel) -> Product:
    result = await session.execute(insert(Product).
                                   values(product_name=product.product_name,
                                          company_id=product.company_id,
                                          price=product.price,
                                          quantity=product.quantity,
                                          currency_type_id=product.currency_type_id).
                                   returning(Product))
    return result.scalar()
