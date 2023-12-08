from fastapi import APIRouter
from app.api.routes import transaction_statuses
from app.api.routes import currency_types
from app.api.routes import companies
from app.api.routes import customers
from app.api.routes import products
from app.api.routes import transactions

router = APIRouter()
router.include_router(transaction_statuses.router, prefix='', tags=['transaction_statuses'])
router.include_router(currency_types.router, prefix='', tags=['currency_types'])
router.include_router(companies.router, prefix='', tags=['companies'])
router.include_router(customers.router, prefix='', tags=['customers'])
router.include_router(products.router, prefix='', tags=['products'])
router.include_router(transactions.router, prefix='', tags=['transactions'])
