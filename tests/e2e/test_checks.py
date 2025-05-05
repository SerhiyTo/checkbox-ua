import pytest
from httpx import AsyncClient, ASGITransport

from src.main import app

CHECK_ID, CHECK_UUID = None, None


@pytest.mark.asyncio
async def test_create_check_success(user_tokens):
    """
    [Successful] Test create check endpoint.
    """
    global CHECK_ID, CHECK_UUID
    access_token, _ = user_tokens

    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test",
        headers={"Authorization": f"Bearer {access_token}"},
    ) as client:
        response = await client.post(
            "/checks",
            json={
                "products": [
                    {
                        "name": "Dji Mavic",
                        "price": 20000,
                        "quantity": 2
                    },
                ],
                "payment": {
                    "type": "cash",
                    "amount": 60000
                }
            },
        )
    assert response.status_code == 201
    assert response.json()["products"][0]["name"] == "Dji Mavic"
    assert response.json()["products"][0]["price"] == 20000
    assert response.json()["products"][0]["quantity"] == 2
    assert response.json()["payment"]["type"] == "cash"
    assert response.json()["payment"]["amount"] == 60000
    assert response.json()["total"] == 40000
    assert response.json()["rest"] == 20000
    assert response.json()["id"] is not None
    assert response.json()["public_uuid"] is not None
    assert response.json()["created_at"] is not None
    CHECK_ID = response.json()["id"]
    CHECK_UUID = response.json()["public_uuid"]


@pytest.mark.asyncio
async def test_get_check_success(user_tokens):
    """
    [Successful] Test get check endpoint.
    """
    access_token, _ = user_tokens

    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test",
        headers={"Authorization": f"Bearer {access_token}"},
    ) as client:
        response = await client.get("/checks")
        response_data = response.json()

    assert response.status_code == 200
    assert isinstance(response_data, list)
    assert len(response_data) > 0


@pytest.mark.asyncio
async def test_get_check_by_id_success(user_tokens):
    """
    [Successful] Test get check by id endpoint.
    """
    access_token, _ = user_tokens

    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test",
        headers={"Authorization": f"Bearer {access_token}"},
    ) as client:
        response = await client.get(f"/checks/{CHECK_ID}")
        response_data = response.json()

    assert response.status_code == 200
    assert response_data["id"] == CHECK_ID
    assert response_data["public_uuid"] == CHECK_UUID


@pytest.mark.asyncio
async def test_get_check_by_uuid_success(user_tokens):
    """
    [Successful] Test get check by uuid endpoint.
    """
    access_token, _ = user_tokens

    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test",
        headers={"Authorization": f"Bearer {access_token}"},
    ) as client:
        response = await client.get(f"/checks/public/{CHECK_UUID}")

    assert response.status_code == 200
