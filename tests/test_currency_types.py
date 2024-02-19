from fastapi import status


'''async def test_get_currency_types(client):
    response = await client.get("/currency_types")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "success",
                               "currency_types": [],
                               'message': None}


async def test_add_currency_type(client):
    response = await client.post(
        "/currency_types",
        json={"currency_type_name": "USD"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    new_currency_type_id = response.json()["currency_type"]["currency_type_id"]

    response = await client.get("/currency_types")
    assert response.status_code == status.HTTP_200_OK
    assert new_currency_type_id == response.json()["currency_types"][0]["currency_type_id"]


async def test_add_currency_type_conflict(client):
    pass'''
