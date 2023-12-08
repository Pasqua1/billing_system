import json
from app.db.queries import companies as queries

from tests.test_main import *


def test_get_companies(test_app, monkeypatch):
    test_data = [
        {"company_id": 1, "company_name": "Yandex"},
        {"company_id": 2, "company_name": "Google"}
    ]

    async def mock_get_companies(db_session):
        return test_data

    monkeypatch.setattr(queries, "get_companies", mock_get_companies)

    response = test_app.get("/companies")
    assert response.status_code == 200
    assert response.json()['companies'] == test_data


def test_add_company(test_app, monkeypatch):
    test_request = {"company_name": "IKEA"}
    test_response = {"company_id": 3, "company_name": "IKEA"}

    async def mock_add_company(db_session, test_request):
        return test_response

    monkeypatch.setattr(queries, "add_company", mock_add_company)

    response = test_app.post("/companies",
                             content=json.dumps(test_request))

    assert response.status_code == 201
    assert response.json()['company'] == test_response
