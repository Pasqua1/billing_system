from fastapi import status

from tests.utils import create_currency_type


async def test_get_company_customers(client, create_currency_type):
    _ = create_currency_type
    response = await client.get("/currency_types")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["currency_types"]) == 1


async def test_add_company(client):
    currency_type = {"currency_type_name": "USD"}

    response = await client.post("/currency_types", json=currency_type)
    response_currency_type = response.json()["currency_type"]["currency_type_name"]

    assert response.status_code == status.HTTP_201_CREATED
    assert response_currency_type == currency_type["currency_type_name"]


async def test_add_company_http_409_conflict(client, create_currency_type):
    _ = create_currency_type

    currency_type = {"currency_type_name": "USD"}
    detail = 'Key (currency_type_name)=(USD) already exists'

    response = await client.post("/currency_types", json=currency_type)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == detail
