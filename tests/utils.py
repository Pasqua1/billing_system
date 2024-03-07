import pytest


@pytest.fixture()
async def create_transaction_status(client):
    response = await client.post("/transaction_statuses", json={"status_name": "NEW"})
    new_status_id = response.json()["transaction_status"]["status_id"]
    return new_status_id


@pytest.fixture()
async def create_currency_type(client):
    response = await client.post("/currency_types", json={"currency_type_name": "USD"})
    new_currency_type_id = response.json()["currency_type"]["currency_type_id"]
    return new_currency_type_id


@pytest.fixture()
async def create_company(client):
    response = await client.post("/companies", json={"company_name": "Google"})
    new_company_id = response.json()["company"]["company_id"]
    return new_company_id


@pytest.fixture()
async def create_customer(client, create_currency_type, create_company):
    currency_type_id = create_currency_type
    company_id = create_company
    response = await client.post("/customers",
                                 json={"customer_name": "Alex",
                                       "company_id": company_id,
                                       "balance": 1000,
                                       "currency_type_id": currency_type_id})
    new_customer_id = response.json()["customer"]["customer_id"]
    return new_customer_id


@pytest.fixture()
async def create_product(client, create_currency_type, create_company):
    currency_type_id = create_currency_type
    company_id = create_company
    response = await client.post("/products",
                                 json={"product_name": "Cakes",
                                       "company_id": company_id,
                                       "price": 10.00,
                                       "quantity": 30,
                                       "currency_type_id": currency_type_id})
    new_product_id = response.json()["product"]["product_id"]
    return new_product_id


@pytest.fixture()
async def create_payment(client, create_transaction_status, create_currency_type, create_company):
    _ = create_transaction_status
    currency_type_id = create_currency_type
    company_id = create_company

    response = await client.post("/customers",
                                 json={"customer_name": "Alex",
                                       "company_id": company_id,
                                       "balance": 1000,
                                       "currency_type_id": currency_type_id})
    customer_id = response.json()["customer"]["customer_id"]

    response = await client.post("/products",
                                 json={"product_name": "Cakes",
                                       "company_id": company_id,
                                       "price": 10,
                                       "quantity": 30,
                                       "currency_type_id": currency_type_id})
    product_id = response.json()["product"]["product_id"]

    response = await client.post("/payment",
                                 json={"quantity": 4,
                                       "customer_id": customer_id,
                                       "product_id": product_id})
    new_transaction_id = response.json()["transaction"]["transaction_id"]
    return new_transaction_id
