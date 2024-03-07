from fastapi import status

from tests.utils import (
    create_transaction_status,
    create_currency_type,
    create_company,
    create_payment
)


async def test_get_transaction(client, create_payment):
    transaction_id = create_payment
    response = await client.get(f"/transactions?transaction_id={transaction_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["transaction"]["transaction_id"] == transaction_id


async def test_get_transactions_of_customer(client, create_payment):
    customer_id = 0
    response = await client.get(f"/transactions/customer?customer_id={customer_id}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["transactions"]) == 0


async def test_get_transactions_in_amount(client, create_payment):
    amount = 1000
    _ = create_payment
    response = await client.get(f"/transactions/amount?amount={amount}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["transactions"]) == 1


async def test_add_payment(
        client,
        create_transaction_status,
        create_currency_type,
        create_company
):
    _ = create_transaction_status
    currency_type_id = create_currency_type
    company_id = create_company

    customer = {"customer_name": "Alex",
                "company_id": company_id,
                "balance": 1000,
                "currency_type_id": currency_type_id}
    response = await client.post("/customers", json=customer)
    customer_id = response.json()["customer"]["customer_id"]

    product = {"product_name": "Cakes",
               "company_id": company_id,
               "price": 10,
               "quantity": 30,
               "currency_type_id": currency_type_id}
    response = await client.post("/products", json=product)
    product_id = response.json()["product"]["product_id"]

    transaction = {"quantity": 4,
                   "customer_id": customer_id,
                   "product_id": product_id}

    response = await client.post("/payment", json=transaction)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["transaction"]["quantity"] == transaction["quantity"]
    assert response.json()["transaction"]["customer_id"] == transaction["customer_id"]
    assert response.json()["transaction"]["product_id"] == transaction["product_id"]

    response = await client.get(f"/customers?customer_id={customer_id}")
    new_balance = float(customer["balance"] - product["price"] * transaction["quantity"])
    response_balance = float(response.json()["customer"]["balance"])
    assert response_balance == new_balance

    response = await client.get(f"/products?product_id={product_id}")
    new_quantity = product["quantity"] - transaction["quantity"]
    assert response.json()["product"]["quantity"] == new_quantity


async def test_add_payment_low_customer_balance(
        client,
        create_transaction_status,
        create_currency_type,
        create_company
):
    _ = create_transaction_status
    currency_type_id = create_currency_type
    company_id = create_company

    customer = {"customer_name": "Alex",
                "company_id": company_id,
                "balance": 0,
                "currency_type_id": currency_type_id}
    response = await client.post("/customers", json=customer)
    customer_id = response.json()["customer"]["customer_id"]

    product = {"product_name": "Cakes",
               "company_id": company_id,
               "price": 1000,
               "quantity": 30,
               "currency_type_id": currency_type_id}
    response = await client.post("/products", json=product)
    product_id = response.json()["product"]["product_id"]

    transaction = {"quantity": 10,
                   "customer_id": customer_id,
                   "product_id": product_id}

    response = await client.post("/payment", json=transaction)

    detail = f'Not enough balance for customer with customer_id = {customer_id}'

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == detail


async def test_add_payment_low_product_quantity(
        client,
        create_transaction_status,
        create_currency_type,
        create_company
):
    _ = create_transaction_status
    currency_type_id = create_currency_type
    company_id = create_company

    customer = {"customer_name": "Alex",
                "company_id": company_id,
                "balance": 100000,
                "currency_type_id": currency_type_id}
    response = await client.post("/customers", json=customer)
    customer_id = response.json()["customer"]["customer_id"]

    product = {"product_name": "Cakes",
               "company_id": company_id,
               "price": 1000,
               "quantity": 30,
               "currency_type_id": currency_type_id}
    response = await client.post("/products", json=product)
    product_id = response.json()["product"]["product_id"]

    transaction = {"quantity": 40,
                   "customer_id": customer_id,
                   "product_id": product_id}

    response = await client.post("/payment", json=transaction)

    detail = f'Not enough quantity for product with product_id = {product_id}'

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == detail


async def test_add_payment_no_new_status(
        client,
        create_currency_type,
        create_company
):
    currency_type_id = create_currency_type
    company_id = create_company

    customer = {"customer_name": "Alex",
                "company_id": company_id,
                "balance": 2222,
                "currency_type_id": currency_type_id}
    response = await client.post("/customers", json=customer)
    customer_id = response.json()["customer"]["customer_id"]

    product = {"product_name": "Cakes",
               "company_id": company_id,
               "price": 12,
               "quantity": 30,
               "currency_type_id": currency_type_id}
    response = await client.post("/products", json=product)
    product_id = response.json()["product"]["product_id"]

    transaction = {"quantity": 10,
                   "customer_id": customer_id,
                   "product_id": product_id}

    response = await client.post("/payment", json=transaction)

    status_name = 'NEW'
    detail = f'There is no transaction_status with name = {status_name}'

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == detail
