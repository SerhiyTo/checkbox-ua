import asyncio
import uuid

import pytest
from faker import Faker

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
