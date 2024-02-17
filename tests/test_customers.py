import json
from app.service.queries import customers as queries
from app.dto.customers import CustomerFullInsertModel

from tests.test_main import test_app


def test_get_customer(test_app, monkeypatch):
    test_data = {"customer_id": 1,
                 "customer_name": "Paul",
                 "company_name": "Yandex",
                 "balance": '1000',
                 "currency_type_name": "USD"}

    async def mock_get_customer(db_session, customer_id):
        return test_data

    monkeypatch.setattr(queries, "get_customer", mock_get_customer)

    response = test_app.get("/customer?customer_id=1")
    assert response.status_code == 200
    assert response.json()['customer'] == test_data


def test_update_balance(test_app, monkeypatch):
    test_customer = CustomerFullInsertModel(
            customer_id=1,
            customer_name="Paul",
            company_id=1,
            balance=1000,
            currency_type_id=1
        )
    test_data = {"customer_id": 1,
                 "customer_name": "Paul",
                 "company_id": 1,
                 "balance": '999',
                 "currency_type_id": 1}

    async def mock_get_customer(db_session, customer_id):
        return test_customer

    async def mock_update_customer_balance(db_session, customer_id, new_balance):
        return test_data

    monkeypatch.setattr(queries, "get_customer", mock_get_customer)
    monkeypatch.setattr(queries, "update_customer_balance", mock_update_customer_balance)

    response = test_app.patch("/customer?customer_id=1&amount=1")
    assert response.status_code == 200
    assert response.json()['customer'] == test_data


def test_get_company_customers(test_app, monkeypatch):
    test_data = [
        {
            "customer_id": 1,
            "customer_name": "Paul",
            "company_name": "Yandex",
            "balance": '1000',
            "currency_type_name": 'USD'
        },
        {
            "customer_id": 2,
            "customer_name": "Paul",
            "company_name": "Yandex",
            "balance": '2000',
            "currency_type_name": 'USD'
        },
        {
            "customer_id": 3,
            "customer_name": "Paul",
            "company_name": "Yandex",
            "balance": '3000',
            "currency_type_name": 'EUR'
        }
    ]

    async def mock_get_company_customers(db_session, company_id):
        return test_data

    monkeypatch.setattr(queries, "get_company_customers", mock_get_company_customers)

    response = test_app.get("/customer/company?company_id=1")
    assert response.status_code == 200
    assert response.json()['customers'] == test_data


def test_add_customer(test_app, monkeypatch):
    test_request = {"customer_name": "Paul",
                    "company_id": 1,
                    "balance": '1000',
                    "currency_type_id": 1}
    test_response = {"customer_id": 1,
                     "customer_name": "Paul",
                     "company_id": 1,
                     "balance": '1000',
                     "currency_type_id": 1}

    async def mock_add_customer(db_session, test_request):
        return test_response

    monkeypatch.setattr(queries, "add_customer", mock_add_customer)

    response = test_app.post("/customer",
                             content=json.dumps(test_request))

    assert response.status_code == 201
    assert response.json()['customer'] == test_response
