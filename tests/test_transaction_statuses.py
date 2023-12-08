import json
from app.db.queries import transaction_statuses as queries

from tests.test_main import *


def test_get_transaction_statuses(test_app, monkeypatch):
    test_data = [
        {"status_id": 1, "status_name": "New"},
        {"status_id": 2, "status_name": "Completed"},
        {"status_id": 3, "status_name": "Rejected"}
    ]

    async def mock_get_transaction_statuses(db_session):
        return test_data

    monkeypatch.setattr(queries, "get_transaction_statuses", mock_get_transaction_statuses)

    response = test_app.get("/transaction_statuses")
    assert response.status_code == 200
    assert response.json()['transaction_statuses'] == test_data


def test_add_transaction_status_success(test_app, monkeypatch):
    test_request = {"status_name": "Pending"}
    test_response = {"status_id": 3, "status_name": "Pending"}

    async def mock_add_transaction_status(db_session, test_request):
        return test_response

    monkeypatch.setattr(queries, "add_transaction_status", mock_add_transaction_status)

    response = test_app.post("/transaction_statuses",
                             content=json.dumps(test_request))

    assert response.status_code == 201
    assert response.json()['transaction_status'] == test_response
