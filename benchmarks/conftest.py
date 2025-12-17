import asyncio
import pytest
from redis import asyncio as aioredis


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def redis_client():
    """Create a Redis client for benchmarking."""
    client = aioredis.from_url("redis://localhost:6379", decode_responses=False)
    yield client
    await client.aclose()
