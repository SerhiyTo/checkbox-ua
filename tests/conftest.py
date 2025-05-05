import asyncio
import uuid

import pytest
import pytest_asyncio
from faker import Faker
from httpx import AsyncClient, ASGITransport

from src.main import app

faker = Faker()
TEST_FIRST_NAME = faker.first_name()
TEST_LAST_NAME = faker.last_name()
TEST_LOGIN = str(f"test-{uuid.uuid4()}")[:64]
TEST_PASSWORD = str(f"test-{uuid.uuid4()}")[:64]


@pytest.fixture(scope="package")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def user_tokens():
    """
    Create user, get tokens and return them.
    """
    auth_data = {
        "login": TEST_LOGIN,
        "password": TEST_PASSWORD,
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/auth/login", json=auth_data)
        response_data = response.json()

    access_token = response_data.get("access_token")
    refresh_token = response_data.get("refresh_token")

    return access_token, refresh_token
