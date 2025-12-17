"""Benchmarks for atomic operations on Redis types."""

import pytest
from pytest_codspeed import BenchmarkFixture

from rapyer import AtomicRedisModel
from rapyer.init import init_rapyer


class BenchmarkModel(AtomicRedisModel):
    """A simple model for benchmarking."""

    name: str = "default"
    count: int = 0
    tags: list[str] = []
    metadata: dict[str, str] = {}


@pytest.fixture(scope="function", autouse=True)
async def setup_redis():
    """Initialize Redis connection for benchmarks."""
    await init_rapyer("redis://localhost:6379")
    yield
    # Cleanup after each benchmark
    keys = await BenchmarkModel.afind_keys()
    if keys:
        await BenchmarkModel.Meta.redis.delete(*keys)


@pytest.mark.asyncio
async def bench_model_creation(benchmark: BenchmarkFixture):
    """Benchmark creating and saving a model."""

    @benchmark
    async def create_model():
        model = BenchmarkModel(name="test", count=100)
        await model.save()
        return model


@pytest.mark.asyncio
async def bench_model_retrieval(benchmark: BenchmarkFixture):
    """Benchmark retrieving a model from Redis."""
    # Setup: Create a model first
    model = BenchmarkModel(name="test", count=100)
    await model.save()
    key = model.key

    @benchmark
    async def get_model():
        return await BenchmarkModel.get(key)


@pytest.mark.asyncio
async def bench_atomic_list_append(benchmark: BenchmarkFixture):
    """Benchmark atomic list append operations."""
    model = BenchmarkModel(name="test")
    await model.save()

    @benchmark
    async def append_to_list():
        await model.tags.aappend("new_tag")


@pytest.mark.asyncio
async def bench_atomic_dict_update(benchmark: BenchmarkFixture):
    """Benchmark atomic dictionary update operations."""
    model = BenchmarkModel(name="test")
    await model.save()

    @benchmark
    async def update_dict():
        await model.metadata.aupdate(key="value", status="active")


@pytest.mark.asyncio
async def bench_atomic_int_increment(benchmark: BenchmarkFixture):
    """Benchmark atomic integer increment operations."""
    model = BenchmarkModel(name="test", count=0)
    await model.save()

    @benchmark
    async def increment_counter():
        await model.count.incrby(1)


@pytest.mark.asyncio
async def bench_model_update(benchmark: BenchmarkFixture):
    """Benchmark updating multiple fields atomically."""
    model = BenchmarkModel(name="test", count=100)
    await model.save()

    @benchmark
    async def update_model():
        await model.aupdate(name="updated", count=200)


@pytest.mark.asyncio
async def bench_lock_context(benchmark: BenchmarkFixture):
    """Benchmark acquiring lock and updating model."""
    model = BenchmarkModel(name="test", count=100)
    await model.save()

    @benchmark
    async def with_lock():
        async with model.lock("benchmark_lock") as locked:
            locked.count += 1
            await locked.save()


@pytest.mark.asyncio
async def bench_pipeline_operations(benchmark: BenchmarkFixture):
    """Benchmark pipeline operations."""
    model = BenchmarkModel(name="test", count=100)
    await model.save()

    @benchmark
    async def with_pipeline():
        async with model.pipeline() as pipelined:
            await pipelined.tags.aappend("tag1")
            await pipelined.metadata.aupdate(key1="value1")
            await pipelined.count.incrby(5)


@pytest.mark.asyncio
async def bench_model_duplication(benchmark: BenchmarkFixture):
    """Benchmark duplicating a model."""
    model = BenchmarkModel(
        name="original", count=100, tags=["tag1", "tag2"], metadata={"key": "value"}
    )
    await model.save()

    @benchmark
    async def duplicate_model():
        return await model.duplicate()


@pytest.mark.asyncio
async def bench_find_all_models(benchmark: BenchmarkFixture):
    """Benchmark finding all models of a type."""
    # Setup: Create multiple models
    models = [BenchmarkModel(name=f"test{i}", count=i) for i in range(10)]
    for model in models:
        await model.save()

    @benchmark
    async def find_all():
        return await BenchmarkModel.afind()
