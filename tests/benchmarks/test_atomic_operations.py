"""
Benchmarks for atomic operations on Redis collections (lists, dicts).
"""
import pytest
from rapyer.base import AtomicRedisModel


class CollectionModel(AtomicRedisModel):
    items: list[str] = []
    numbers: list[int] = []
    metadata: dict[str, str] = {}
    counters: dict[str, int] = {}


@pytest.mark.asyncio
@pytest.mark.benchmark
async def test_list_append_performance():
    """Benchmark atomic list append operations."""
    model = CollectionModel()
    await model.save()
    
    await model.items.aappend("item1")
    await model.items.aappend("item2")
    await model.items.aappend("item3")
    
    loaded = await CollectionModel.get(model.key)
    assert len(loaded.items) == 3


@pytest.mark.asyncio
@pytest.mark.benchmark
async def test_list_extend_performance():
    """Benchmark atomic list extend operations."""
    model = CollectionModel()
    await model.save()
    
    await model.numbers.aextend([1, 2, 3, 4, 5])
    
    loaded = await CollectionModel.get(model.key)
    assert len(loaded.numbers) == 5


@pytest.mark.asyncio
@pytest.mark.benchmark
async def test_dict_update_performance():
    """Benchmark atomic dict update operations."""
    model = CollectionModel()
    await model.save()
    
    await model.metadata.aupdate(key1="value1", key2="value2", key3="value3")
    
    loaded = await CollectionModel.get(model.key)
    assert len(loaded.metadata) == 3
    assert loaded.metadata["key1"] == "value1"


@pytest.mark.asyncio
@pytest.mark.benchmark
async def test_dict_set_item_performance():
    """Benchmark atomic dict item setting."""
    model = CollectionModel()
    await model.save()
    
    await model.counters.aset("counter1", 100)
    await model.counters.aset("counter2", 200)
    await model.counters.aset("counter3", 300)
    
    loaded = await CollectionModel.get(model.key)
    assert loaded.counters["counter1"] == 100


@pytest.mark.asyncio
@pytest.mark.benchmark
async def test_multiple_atomic_operations_performance():
    """Benchmark multiple sequential atomic operations."""
    model = CollectionModel()
    await model.save()
    
    await model.items.aappend("item1")
    await model.numbers.aextend([1, 2, 3])
    await model.metadata.aupdate(status="active", type="test")
    await model.counters.aset("score", 100)
    
    loaded = await CollectionModel.get(model.key)
    assert len(loaded.items) == 1
    assert len(loaded.numbers) == 3
    assert len(loaded.metadata) == 2
    assert loaded.counters["score"] == 100
