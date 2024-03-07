from fastapi import status

from tests.utils import create_company


async def test_get_company_customers(client, create_company):
    _ = create_company
    response = await client.get("/companies")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["companies"]) == 1


async def test_add_company(client):
    company = {"company_name": "Google"}

    response = await client.post("/companies", json=company)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["company"]["company_name"] == company["company_name"]


async def test_add_company_http_409_conflict(client, create_company):
    _ = create_company

    company = {"company_name": "Google"}
    detail = 'Key (company_name)=(Google) already exists'

    response = await client.post("/companies", json=company)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == detail
