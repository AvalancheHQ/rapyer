import asyncio
import os
import pytest
from redis.asyncio import Redis
from rapyer.config import RedisConfig
from rapyer.base import AtomicRedisModel


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def redis_client():
    """Create a Redis client for benchmarking."""
    # Use environment variables for Redis configuration to support CI
    host = os.environ.get("REDIS_HOST", "localhost")
    port = int(os.environ.get("REDIS_PORT", "6370"))
    db = int(os.environ.get("REDIS_DB", "0"))
    
    client = Redis(host=host, port=port, decode_responses=False, db=db)
    yield client
    await client.aclose()


@pytest.fixture(autouse=True)
async def setup_redis_for_models(redis_client):
    """Configure Redis client for all models."""
    AtomicRedisModel.Meta = RedisConfig(redis=redis_client)
    yield
    # Cleanup after each test
    await redis_client.flushdb()
