"""Benchmarks for pipeline operations in Rapyer.

These benchmarks measure the performance of pipeline context managers
that batch multiple operations into a single atomic transaction.
"""

import pytest

from tests.models.collection_types import MixedTypesModel, PipelineTestModel


@pytest.mark.asyncio
async def test_benchmark_pipeline_list_operations(benchmark):
    """Benchmark pipeline with multiple list operations."""
    model = MixedTypesModel()
    await model.save()

    @benchmark
    async def bench():
        async with model.pipeline():
            await model.int_list.aappend(1)
            await model.int_list.aappend(2)
            await model.int_list.aappend(3)


@pytest.mark.asyncio
async def test_benchmark_pipeline_dict_operations(benchmark):
    """Benchmark pipeline with multiple dict operations."""
    model = MixedTypesModel()
    await model.save()

    @benchmark
    async def bench():
        async with model.pipeline():
            await model.str_dict.aset_item("key1", "value1")
            await model.str_dict.aset_item("key2", "value2")
            await model.str_dict.aset_item("key3", "value3")


@pytest.mark.asyncio
async def test_benchmark_pipeline_mixed_operations(benchmark):
    """Benchmark pipeline with mixed operation types."""
    model = MixedTypesModel()
    await model.save()

    @benchmark
    async def bench():
        async with model.pipeline():
            await model.int_list.aappend(42)
            await model.str_dict.aset_item("status", "active")
            await model.bool_dict.aset_item("enabled", True)


@pytest.mark.asyncio
async def test_benchmark_pipeline_comprehensive(benchmark):
    """Benchmark pipeline with comprehensive model operations."""
    model = PipelineTestModel()
    await model.save()

    @benchmark
    async def bench():
        async with model.pipeline():
            await model.metadata.aupdate(key1="value1", key2="value2")
            await model.config.aupdate(setting1=1, setting2=2)


@pytest.mark.asyncio
async def test_benchmark_without_pipeline(benchmark):
    """Benchmark operations without pipeline for comparison."""
    model = MixedTypesModel()
    await model.save()

    @benchmark
    async def bench():
        await model.int_list.aappend(1)
        await model.int_list.aappend(2)
        await model.int_list.aappend(3)
