from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.products import Product, ProductModel


async def get_product(session: AsyncSession, product_id: int) -> Product:
    result = await session.execute(select(Product).
                                   where(Product.product_id==product_id))
    return result.scalar()


async def update_product_quantity(session: AsyncSession, 
                                 product_id: int, 
                                 amount: int) -> Product:
    product = await get_product(session, product_id)
    if product:
        new_quantity = product.quantity - amount
        result = await session.execute(update(Product).
                                    where(Product.product_id==product_id).
                                    values(quantity=new_quantity).
                                    returning(Product))
        return result.scalar()
    return None


async def get_products(session: AsyncSession, price: int) -> list[ProductModel]:
    result = await session.execute(select(Product).where(Product.price<=price))
    products = result.scalars().all()
    products = [
        ProductModel(product_id=product.product_id,
                     product_name=product.product_name,
                     price=product.price,
                     quantity=product.quantity,
                     currency_type_id=product.currency_type_id) for product in products
    ]
    return products


async def add_product(session: AsyncSession, product: ProductModel) -> Product:
    result = await session.execute(insert(Product).
                                 values(product_name=product.product_name,
                                        price=product.price,
                                        quantity=product.quantity,
                                        currency_type_id=product.currency_type_id).
                                 returning(Product))
    return result.scalar()
