"""Benchmarks for Redis type operations."""

import pytest
from pytest_codspeed import BenchmarkFixture

from rapyer import AtomicRedisModel
from rapyer.init import init_rapyer


class StringModel(AtomicRedisModel):
    """Model with string field for benchmarking."""

    text: str = "default"


class IntModel(AtomicRedisModel):
    """Model with integer field for benchmarking."""

    value: int = 0


class ListModel(AtomicRedisModel):
    """Model with list field for benchmarking."""

    items: list[str] = []


class DictModel(AtomicRedisModel):
    """Model with dict field for benchmarking."""

    data: dict[str, str] = {}


@pytest.fixture(scope="function", autouse=True)
async def setup_redis():
    """Initialize Redis connection for benchmarks."""
    await init_rapyer("redis://localhost:6379")
    yield
    # Cleanup
    for model_class in [StringModel, IntModel, ListModel, DictModel]:
        keys = await model_class.afind_keys()
        if keys:
            await model_class.Meta.redis.delete(*keys)


@pytest.mark.asyncio
async def bench_string_assignment(benchmark: BenchmarkFixture):
    """Benchmark string field assignment."""
    model = StringModel(text="initial")
    await model.save()

    @benchmark
    def assign_string():
        model.text = "new value"


@pytest.mark.asyncio
async def bench_int_operations(benchmark: BenchmarkFixture):
    """Benchmark integer arithmetic operations."""
    model = IntModel(value=100)
    await model.save()

    @benchmark
    def int_arithmetic():
        model.value += 10
        model.value -= 5
        model.value *= 2


@pytest.mark.asyncio
async def bench_list_extend(benchmark: BenchmarkFixture):
    """Benchmark list extend operation."""
    model = ListModel(items=["item1", "item2"])
    await model.save()

    @benchmark
    async def extend_list():
        await model.items.aextend(["item3", "item4", "item5"])


@pytest.mark.asyncio
async def bench_list_pop(benchmark: BenchmarkFixture):
    """Benchmark list pop operation."""
    model = ListModel(items=["item1", "item2", "item3", "item4", "item5"])
    await model.save()

    @benchmark
    async def pop_list():
        await model.items.apop()


@pytest.mark.asyncio
async def bench_dict_multi_update(benchmark: BenchmarkFixture):
    """Benchmark updating multiple dictionary keys."""
    model = DictModel(data={"key1": "value1"})
    await model.save()

    @benchmark
    async def update_multiple_keys():
        await model.data.aupdate(
            key2="value2", key3="value3", key4="value4", key5="value5"
        )


@pytest.mark.asyncio
async def bench_dict_key_deletion(benchmark: BenchmarkFixture):
    """Benchmark deleting dictionary keys."""
    model = DictModel(data={"key1": "value1", "key2": "value2", "key3": "value3"})
    await model.save()

    @benchmark
    async def delete_key():
        await model.data.adelete_key("key1")


@pytest.mark.asyncio
async def bench_string_concatenation(benchmark: BenchmarkFixture):
    """Benchmark string concatenation."""
    model = StringModel(text="Hello")

    @benchmark
    def concat_strings():
        result = model.text + " World"
        return result


@pytest.mark.asyncio
async def bench_list_contains(benchmark: BenchmarkFixture):
    """Benchmark list membership check."""
    model = ListModel(items=[f"item{i}" for i in range(100)])

    @benchmark
    def check_contains():
        return "item50" in model.items


@pytest.mark.asyncio
async def bench_dict_get(benchmark: BenchmarkFixture):
    """Benchmark dictionary get operation."""
    model = DictModel(data={f"key{i}": f"value{i}" for i in range(100)})

    @benchmark
    def get_dict_value():
        return model.data.get("key50")
