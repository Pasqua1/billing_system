from decimal import Decimal
from fastapi import status

from tests.utils import create_currency_type, create_company, create_customer


async def test_get_customer(client, create_customer):
    customer_id = create_customer

    response = await client.get(f"/customers?customer_id={customer_id}")
    assert response.status_code == status.HTTP_200_OK
    assert customer_id == response.json()["customer"]["customer_id"]


async def test_update_balance(client, create_customer):
    customer_id = create_customer

    new_balance = Decimal(2000.00)

    response = await client.patch(f"/customers?customer_id={customer_id}&new_balance={new_balance}")

    assert response.status_code == 200
    assert 2000.00 == Decimal(response.json()["customer"]["balance"])


async def test_get_company_customers(client):
    response = await client.get(f"/customers/company?company_id=99")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["customers"]) == 0


async def test_add_customer(client, create_currency_type, create_company):
    currency_type_id = create_currency_type

    company_id = create_company

    customer = {"customer_name": "Alice",
                "company_id": company_id,
                "balance": '2000.00',
                "currency_type_id": currency_type_id}

    response = await client.post("/customers", json=customer)

    assert response.status_code == status.HTTP_201_CREATED

    customer_id = response.json()["customer"]["customer_id"]

    response = await client.get(f"/customers?customer_id={customer_id}")
    assert response.status_code == status.HTTP_200_OK
    assert customer_id == response.json()["customer"]["customer_id"]
    assert customer["customer_name"] == response.json()["customer"]["customer_name"]
    assert customer["company_id"] == response.json()["customer"]["company_id"]
    assert customer["balance"] == response.json()["customer"]["balance"]
    assert customer["currency_type_id"] == response.json()["customer"]["currency_type_id"]
