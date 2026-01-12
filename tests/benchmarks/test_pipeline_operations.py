"""
Benchmarks for pipeline batch operations.
"""
import pytest
from rapyer.base import AtomicRedisModel


class PipelineModel(AtomicRedisModel):
    name: str = ""
    score: int = 0
    tags: list[str] = []
    metadata: dict[str, str] = {}


@pytest.mark.asyncio
@pytest.mark.benchmark
async def test_pipeline_multiple_operations_performance():
    """Benchmark pipeline with multiple operations."""
    model = PipelineModel(name="test", score=0)
    await model.save()
    
    async with model.pipeline() as pipelined_model:
        await pipelined_model.tags.aappend("tag1")
        await pipelined_model.tags.aappend("tag2")
        await pipelined_model.metadata.aupdate(status="active", level="premium")
    
    loaded = await PipelineModel.get(model.key)
    assert len(loaded.tags) == 2
    assert loaded.metadata["status"] == "active"


@pytest.mark.asyncio
@pytest.mark.benchmark
async def test_pipeline_batch_updates_performance():
    """Benchmark pipeline for batch updates."""
    model = PipelineModel(name="batch_test", score=100)
    await model.save()
    
    async with model.pipeline() as pipelined_model:
        for i in range(10):
            await pipelined_model.tags.aappend(f"tag_{i}")
    
    loaded = await PipelineModel.get(model.key)
    assert len(loaded.tags) == 10
