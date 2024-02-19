'''import json

from decimal import Decimal
from app.service.queries import transactions as queries
from app.service.queries import customers as customers_queries
from app.service.queries import products as products_queries
from app.dto.products import ProductFullModel
from app.dto.customers import CustomerFullModel

from tests.test_main import *


def test_get_transaction_by_transaction_id(test_app, monkeypatch):
    test_data = {"transaction_id": 1,
                 "date_create": "2023-12-08T07:45:45.149000Z",
                 "amount": "450",
                 "status_name": 'New',
                 "currency_type_name": "USD",
                 "customer_name": "Paul",
                 "product_name": 'Cookies',
                 "number_of_products": 15}

    async def mock_get_transaction_by_transaction_id(db_session, transaction_id):
        return test_data

    monkeypatch.setattr(queries, "get_transaction_by_transaction_id", mock_get_transaction_by_transaction_id)

    response = test_app.get("/transaction?transaction_id=1")
    assert response.status_code == 200
    assert response.json()['transaction'] == test_data


def test_get_transactions_of_customer(test_app, monkeypatch):
    test_data = [
        {
            "transaction_id": 1,
            "date_create": "2023-12-07T07:45:45.149000Z",
            "amount": "300",
            "status_name": 'New',
            "currency_type_name": "USD",
            "customer_name": "Paul",
            "product_name": 'Cookies',
            "number_of_products": 10
        },
        {
            "transaction_id": 2,
            "date_create": "2023-12-08T07:45:45.149000Z",
            "amount": "450",
            "status_name": 'New',
            "currency_type_name": "USD",
            "customer_name": "Paul",
            "product_name": 'Cookies',
            "number_of_products": 15
        },
        {
            "transaction_id": 3,
            "date_create": "2023-12-06T07:45:45.149000Z",
            "amount": "600",
            "status_name": 'New',
            "currency_type_name": "USD",
            "customer_name": "Paul",
            "product_name": 'Cookies',
            "number_of_products": 20
        }
    ]

    async def mock_get_transactions_of_customer(db_session, customer_id):
        return test_data

    monkeypatch.setattr(queries, "get_transactions_of_customer", mock_get_transactions_of_customer)

    response = test_app.get("/transactions/customer?customer_id=1")
    assert response.status_code == 200
    assert response.json()['transactions'] == test_data


def test_get_transaction_in_range(test_app, monkeypatch):
    test_data = [
        {
            "transaction_id": 1,
            "date_create": "2023-12-07T07:45:45.149000Z",
            "amount": "300",
            "status_name": 'New',
            "currency_type_name": "USD",
            "customer_name": "Paul",
            "product_name": 'Cookies',
            "number_of_products": 10
        },
        {
            "transaction_id": 2,
            "date_create": "2023-12-08T07:45:45.149000Z",
            "amount": "450",
            "status_name": 'New',
            "currency_type_name": "USD",
            "customer_name": "Paul",
            "product_name": 'Cookies',
            "number_of_products": 15
        }
    ]

    async def mock_get_transaction_in_range(db_session, amount):
        return test_data

    monkeypatch.setattr(queries, "get_transactions_in_range", mock_get_transaction_in_range)

    response = test_app.get("/transactions?amount=500")
    assert response.status_code == 200
    assert response.json()['transactions'] == test_data


def test_add_payment(test_app, monkeypatch):
    test_request = {
        "amount": "450",
        "status_id": 1,
        "currency_type_id": 1,
        "customer_id": 1,
        "product_id": 1,
        "number_of_products": 15
    }
    test_response = {
        "transaction_id": 2,
        "date_create": "2023-12-08T07:45:45.149000Z",
        "amount": "450",
        "status_id": 1,
        "currency_type_id": 1,
        "customer_id": 1,
        "product_id": 1,
        "number_of_products": 15
    }
    test_customer = CustomerFullModel(
        customer_id=1,
        customer_name="Paul",
        company_name="Yandex",
        balance=Decimal(1000),
        currency_type_name="USD"
    )

    test_customer_data = {"customer_id": 1,
                          "customer_name": "Paul",
                          "company_name": "Yandex",
                          "balance": '999',
                          "currency_type_name": "USD"}

    test_product = ProductFullModel(
        product_id=1,
        product_name="Paul",
        company_name="Yandex",
        price=Decimal(1000),
        quantity=1000,
        currency_type_name="USD"
    )

    test_product_data = {"product_id": 1,
                         "product_name": "Paul",
                         "company_name": "Yandex",
                         "price": '999',
                         "quantity": 15,
                         "currency_type_name": "USD"}

    async def mock_get_customer(db_session, customer_id):
        return test_customer

    async def mock_get_product(db_session, product_id):
        return test_product

    async def mock_update_customer_balance(db_session, customer_id, new_balance):
        return test_customer_data

    async def mock_update_product_quantity(db_session, product_id, new_quantity):
        return test_product_data

    async def mock_add_payment(db_session, test_request):
        return test_response

    monkeypatch.setattr(customers_queries, 'get_customer', mock_get_customer)
    monkeypatch.setattr(products_queries, 'get_product', mock_get_product)
    monkeypatch.setattr(customers_queries, 'update_customer_balance', mock_update_customer_balance)
    monkeypatch.setattr(products_queries, 'update_product_quantity', mock_update_product_quantity)
    monkeypatch.setattr(queries, "add_payment", mock_add_payment)

    response = test_app.post("/payment",
                             content=json.dumps(test_request))

    assert response.status_code == 201
    assert response.json()['transaction'] == test_response
'''