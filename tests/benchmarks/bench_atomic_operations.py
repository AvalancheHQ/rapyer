"""Benchmarks for atomic operations in Rapyer.

These benchmarks measure the performance of core atomic operations
that prevent race conditions and ensure data consistency.
"""

import pytest

from tests.models.collection_types import IntListModel, StrDictModel, MixedTypesModel


@pytest.mark.asyncio
async def test_benchmark_list_append(benchmark):
    """Benchmark atomic list append operation."""
    model = IntListModel()
    await model.save()

    @benchmark
    async def bench():
        await model.items.aappend(42)


@pytest.mark.asyncio
async def test_benchmark_list_extend(benchmark):
    """Benchmark atomic list extend operation."""
    model = IntListModel()
    await model.save()
    values = list(range(10))

    @benchmark
    async def bench():
        await model.items.aextend(values)


@pytest.mark.asyncio
async def test_benchmark_list_pop(benchmark):
    """Benchmark atomic list pop operation."""
    model = IntListModel()
    await model.save()
    # Pre-populate the list
    await model.items.aextend(list(range(100)))

    @benchmark
    async def bench():
        await model.items.apop()


@pytest.mark.asyncio
async def test_benchmark_list_insert(benchmark):
    """Benchmark atomic list insert operation."""
    model = IntListModel()
    await model.save()
    await model.items.aextend(list(range(10)))

    @benchmark
    async def bench():
        await model.items.ainsert(5, 999)


@pytest.mark.asyncio
async def test_benchmark_dict_update(benchmark):
    """Benchmark atomic dict update operation."""
    model = StrDictModel()
    await model.save()

    @benchmark
    async def bench():
        await model.metadata.aupdate(key1="value1", key2="value2", key3="value3")


@pytest.mark.asyncio
async def test_benchmark_dict_setitem(benchmark):
    """Benchmark atomic dict setitem operation."""
    model = StrDictModel()
    await model.save()

    @benchmark
    async def bench():
        await model.metadata.aset_item("benchmark_key", "benchmark_value")


@pytest.mark.asyncio
async def test_benchmark_dict_pop(benchmark):
    """Benchmark atomic dict pop operation."""
    model = StrDictModel()
    await model.save()
    # Pre-populate the dict
    await model.metadata.aupdate(**{f"key{i}": f"value{i}" for i in range(100)})

    @benchmark
    async def bench():
        await model.metadata.apop("key50")


@pytest.mark.asyncio
async def test_benchmark_mixed_type_operations(benchmark):
    """Benchmark mixed atomic operations on a single model."""
    model = MixedTypesModel()
    await model.save()

    @benchmark
    async def bench():
        await model.str_list.aappend("test_string")
        await model.int_list.aappend(42)
        await model.bool_dict.aset_item("active", True)
        await model.mixed_dict.aupdate(key="value")
