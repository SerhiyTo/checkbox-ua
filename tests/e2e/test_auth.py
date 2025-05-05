import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app
from tests.conftest import TEST_LOGIN, TEST_PASSWORD, TEST_FIRST_NAME, TEST_LAST_NAME


@pytest.mark.asyncio
async def test_register_user_success():
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/auth/register",
            json={
                "first_name": TEST_FIRST_NAME,
                "last_name": TEST_LAST_NAME,
                "login": TEST_LOGIN,
                "password": TEST_PASSWORD,
            },
        )
    assert response.status_code == 201
    assert response.json()["login"] == TEST_LOGIN
    assert response.json()["first_name"] == TEST_FIRST_NAME
    assert response.json()["last_name"] == TEST_LAST_NAME


@pytest.mark.asyncio
async def test_register_user_fail():
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/auth/register",
            json={
                "first_name": TEST_FIRST_NAME,
                "last_name": TEST_LAST_NAME,
                "login": TEST_LOGIN,
                "password": TEST_PASSWORD,
            },
        )
    assert response.status_code == 409
    assert response.json()["detail"] == f"User with username '{TEST_LOGIN}' already exists."


@pytest.mark.asyncio
async def test_login_user_success():
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/auth/login",
            json={
                "login": TEST_LOGIN,
                "password": TEST_PASSWORD,
            },
        )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


@pytest.mark.asyncio
async def test_login_user_fail():
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/auth/login",
            json={
                "login": TEST_LOGIN,
                "password": "wrong_password",
            },
        )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid password."
