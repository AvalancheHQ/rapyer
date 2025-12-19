"""Benchmarks for lock operations in Rapyer.

These benchmarks measure the performance of lock context managers
used for complex multi-field updates and preventing race conditions.
"""

import pytest

from tests.models.functionality_types import LockUpdateTestModel


@pytest.mark.asyncio
async def test_benchmark_lock_context_simple(benchmark):
    """Benchmark lock context manager with simple update."""
    model = LockUpdateTestModel(name="test", value=0)
    await model.save()

    @benchmark
    async def bench():
        async with model.lock("update") as locked_model:
            locked_model.value += 1


@pytest.mark.asyncio
async def test_benchmark_lock_context_multi_field(benchmark):
    """Benchmark lock context manager with multiple field updates."""
    model = LockUpdateTestModel(name="test", value=0)
    await model.save()

    @benchmark
    async def bench():
        async with model.lock("multi_update") as locked_model:
            locked_model.value += 1
            locked_model.name = "updated"


@pytest.mark.asyncio
async def test_benchmark_without_lock(benchmark):
    """Benchmark update without lock for comparison."""
    model = LockUpdateTestModel(name="test", value=0)
    await model.save()

    @benchmark
    async def bench():
        model.value += 1
        await model.save()
