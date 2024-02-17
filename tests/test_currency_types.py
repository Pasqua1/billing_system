import json
from app.service.queries import currency_types as queries

from tests.test_main import test_app


def test_get_currency_types(test_app, monkeypatch):
    test_data = [
        {"currency_type_id": 1, "currency_type_name": "USD"},
        {"currency_type_id": 2, "currency_type_name": "EUR"}
    ]

    async def mock_get_currency_types(db_session):
        return test_data

    monkeypatch.setattr(queries, "get_currency_types", mock_get_currency_types)

    response = test_app.get("/currency_types")
    assert response.status_code == 200
    assert response.json()['currency_types'] == test_data


def test_add_currency_type(test_app, monkeypatch):
    test_request = {"currency_type_name": "IKEA"}
    test_response = {"currency_type_id": 3, "currency_type_name": "IKEA"}

    async def mock_add_currency_type(db_session, test_request):
        return test_response

    monkeypatch.setattr(queries, "add_currency_type", mock_add_currency_type)

    response = test_app.post("/currency_types",
                             content=json.dumps(test_request))

    assert response.status_code == 201
    assert response.json()['currency_type'] == test_response
