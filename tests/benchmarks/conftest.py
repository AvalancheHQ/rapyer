import os

import pytest_asyncio

import rapyer

from tests.models.collection_types import (
    MixedTypesModel,
    IntListModel,
    StrDictModel,
)
from tests.models.simple_types import IntModel, StrModel
from tests.models.specialized import UserModel


@pytest_asyncio.fixture
async def redis_client():
    meta_redis = rapyer.AtomicRedisModel.Meta.redis
    db_num = os.getenv("REDIS_DB", "0")
    redis = meta_redis.from_url(
        f"redis://localhost:6370/{db_num}", decode_responses=True
    )
    await redis.flushdb()
    yield redis
    await redis.flushdb()


@pytest_asyncio.fixture(autouse=True)
async def benchmark_redis_client(redis_client):
    # Configure Redis client for benchmark models
    redis_models = [
        MixedTypesModel,
        IntListModel,
        StrDictModel,
        IntModel,
        StrModel,
        UserModel,
    ]

    for model in redis_models:
        model.Meta.redis = redis_client

    yield redis_client
    await redis_client.aclose()
