"""
Benchmarks for lock context manager operations.
"""
import pytest
from rapyer.base import AtomicRedisModel


class LockModel(AtomicRedisModel):
    balance: int = 0
    transaction_count: int = 0
    tags: list[str] = []


@pytest.mark.asyncio
@pytest.mark.benchmark
async def test_lock_context_performance():
    """Benchmark lock context manager."""
    model = LockModel(balance=1000)
    await model.save()
    
    async with model.lock("transaction") as locked_model:
        locked_model.balance -= 50
        locked_model.transaction_count += 1
    
    loaded = await LockModel.get(model.key)
    assert loaded.balance == 950
    assert loaded.transaction_count == 1


@pytest.mark.asyncio
@pytest.mark.benchmark
async def test_lock_with_atomic_operations_performance():
    """Benchmark lock with atomic operations."""
    model = LockModel(balance=500)
    await model.save()
    
    async with model.lock("update") as locked_model:
        locked_model.balance += 100
        await locked_model.tags.aappend("completed")
        locked_model.transaction_count += 1
    
    loaded = await LockModel.get(model.key)
    assert loaded.balance == 600
    assert "completed" in loaded.tags
