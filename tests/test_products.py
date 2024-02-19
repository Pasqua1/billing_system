import json
from app.service.queries import products as queries

from tests.test_main import test_app


'''def test_get_products(test_app, monkeypatch):
    test_data = [
        {
            "product_id": 1,
            "product_name": "Cakes",
            "company_name": "Yandex",
            "price": '1000',
            "quantity": 30,
            "currency_type_name": 'USD'
        },
        {
            "product_id": 2,
            "product_name": "Cookies",
            "company_name": "Yandex",
            "price": '20',
            "quantity": 2000,
            "currency_type_name": 'USD'
        },
        {
            "product_id": 3,
            "product_name": "Candies",
            "company_name": "Yandex",
            "price": '10',
            "quantity": 3000,
            "currency_type_name": 'USD'
        }
    ]

    price = '4000'

    async def mock_get_products(db_session, price):
        return test_data

    monkeypatch.setattr(queries, "get_products", mock_get_products)

    response = test_app.get("/product?price=4000")
    assert response.status_code == 200
    assert response.json()['products'] == test_data


def test_add_product(test_app, monkeypatch):
    test_request = {
            "product_name": "Cakes",
            "company_id": 1,
            "price": '1000',
            "quantity": 3000,
            "currency_type_id": 1
        }
    test_response = {
            "product_id": 1,
            "product_name": "Cakes",
            "company_id": 1,
            "price": '1000',
            "quantity": 3000,
            "currency_type_id": 1
        }

    async def mock_add_product(db_session, test_request):
        return test_response

    monkeypatch.setattr(queries, "add_product", mock_add_product)

    response = test_app.post("/product",
                             content=json.dumps(test_request))

    assert response.status_code == 201
    assert response.json()['product'] == test_response'''
