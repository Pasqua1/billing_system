from fastapi import status

from tests.utils import create_transaction_status


async def test_get_company_customers(client, create_transaction_status):
    _ = create_transaction_status
    response = await client.get("/transaction_statuses")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["transaction_statuses"]) == 1


async def test_add_company(client):
    transaction_status = {"status_name": "NEW"}

    response = await client.post("/transaction_statuses", json=transaction_status)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["transaction_status"]["status_name"] == transaction_status["status_name"]


async def test_add_company_http_409_conflict(client, create_transaction_status):
    _ = create_transaction_status

    transaction_status = {"status_name": "NEW"}
    detail = 'Key (status_name)=(NEW) already exists'

    response = await client.post("/transaction_statuses", json=transaction_status)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == detail
