"""Benchmarks for core model operations in Rapyer.

These benchmarks measure the performance of basic model lifecycle operations
such as save, load, and deletion.
"""

import pytest

from tests.models.simple_types import IntModel, StrModel
from tests.models.specialized import UserModel


@pytest.mark.asyncio
async def test_benchmark_model_save(benchmark):
    """Benchmark model save operation."""
    
    @benchmark
    async def bench():
        model = IntModel(count=42, score=100)
        await model.save()


@pytest.mark.asyncio
async def test_benchmark_model_load(benchmark):
    """Benchmark model load operation."""
    # Setup: Create and save a model
    model = IntModel(count=42, score=100)
    await model.save()
    key = model.key

    @benchmark
    async def bench():
        loaded_model = await IntModel.get(key)
        return loaded_model


@pytest.mark.asyncio
async def test_benchmark_model_delete(benchmark):
    """Benchmark model delete operation."""
    
    @benchmark
    async def bench():
        model = IntModel(count=42, score=100)
        await model.save()
        await model.delete()


@pytest.mark.asyncio
async def test_benchmark_model_save_with_string(benchmark):
    """Benchmark model save operation with string data."""
    
    @benchmark
    async def bench():
        model = StrModel(name="test_name", description="test_description")
        await model.save()


@pytest.mark.asyncio
async def test_benchmark_model_save_complex(benchmark):
    """Benchmark save operation for complex model with multiple fields."""
    
    @benchmark
    async def bench():
        user = UserModel()
        await user.save()


@pytest.mark.asyncio
async def test_benchmark_model_update(benchmark):
    """Benchmark model update operation."""
    model = StrModel(name="initial_name", description="initial_description")
    await model.save()

    @benchmark
    async def bench():
        model.name = "updated_name"
        await model.save()


@pytest.mark.asyncio
async def test_benchmark_batch_save(benchmark):
    """Benchmark batch save operations."""
    
    @benchmark
    async def bench():
        models = [IntModel(count=i, score=i*10) for i in range(10)]
        for model in models:
            await model.save()


@pytest.mark.asyncio
async def test_benchmark_batch_load(benchmark):
    """Benchmark batch load operations."""
    # Setup: Create and save multiple models
    models = [IntModel(count=i, score=i*10) for i in range(10)]
    for model in models:
        await model.save()
    keys = [model.key for model in models]

    @benchmark
    async def bench():
        loaded_models = []
        for key in keys:
            model = await IntModel.get(key)
            loaded_models.append(model)
        return loaded_models
