from fastapi import status

from tests.utils import create_currency_type, create_company, create_product


async def test_add_product(client, create_currency_type, create_company):
    currency_type_id = create_currency_type

    company_id = create_company

    product = {"product_name": "Cakes",
               "company_id": company_id,
               "price": "1000.00",
               "quantity": 30,
               "currency_type_id": currency_type_id}

    response = await client.post("/products", json=product)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["product"]["product_name"] == product["product_name"]
    assert response.json()["product"]["company_id"] == product["company_id"]
    assert response.json()["product"]["price"] == product["price"]
    assert response.json()["product"]["quantity"] == product["quantity"]
    assert response.json()["product"]["currency_type_id"] == product["currency_type_id"]


async def test_add_product_negative_price_http_409_conflict(
        client,
        create_currency_type,
        create_company
):
    currency_type_id = create_currency_type

    company_id = create_company

    detail = "price should not be less than 0"

    product = {"product_name": "Cakes",
               "company_id": company_id,
               "price": "-1000.00",
               "quantity": 30,
               "currency_type_id": currency_type_id}

    response = await client.post("/products", json=product)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == detail


async def test_add_product_negative_quantity_http_409_conflict(
        client,
        create_currency_type,
        create_company
):
    currency_type_id = create_currency_type

    company_id = create_company

    detail = "quantity should not be less than 0"

    product = {"product_name": "Cakes",
               "company_id": company_id,
               "price": "1000.00",
               "quantity": -30,
               "currency_type_id": currency_type_id}

    response = await client.post("/products", json=product)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == detail


async def test_get_products(client, create_product):
    _ = create_product
    price = 2000
    response = await client.get(f"/products?price={price}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["products"]) == 1
