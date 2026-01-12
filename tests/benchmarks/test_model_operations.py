"""
Benchmarks for basic Rapyer model operations including creation, save, load, and updates.
"""
import pytest
from rapyer.base import AtomicRedisModel


class UserModel(AtomicRedisModel):
    name: str = ""
    age: int = 0
    email: str = ""
    active: bool = True
    tags: list[str] = []
    metadata: dict[str, str] = {}


@pytest.mark.asyncio
@pytest.mark.benchmark
async def test_model_creation_performance():
    """Benchmark model instantiation."""
    user = UserModel(name="John Doe", age=30, email="john@example.com")
    assert user.name == "John Doe"


@pytest.mark.asyncio
@pytest.mark.benchmark
async def test_model_save_performance():
    """Benchmark saving a model to Redis."""
    user = UserModel(name="Jane Smith", age=25, email="jane@example.com")
    await user.save()
    assert user.key


@pytest.mark.asyncio
@pytest.mark.benchmark
async def test_model_get_performance():
    """Benchmark loading a model from Redis."""
    user = UserModel(name="Bob Johnson", age=35, email="bob@example.com")
    await user.save()
    
    loaded_user = await UserModel.get(user.key)
    assert loaded_user.name == "Bob Johnson"


@pytest.mark.asyncio
@pytest.mark.benchmark
async def test_model_update_performance():
    """Benchmark updating model fields."""
    user = UserModel(name="Alice Brown", age=28, email="alice@example.com")
    await user.save()
    
    user.name = "Alice Updated"
    user.age = 29
    await user.save()
    
    loaded_user = await UserModel.get(user.key)
    assert loaded_user.name == "Alice Updated"
    assert loaded_user.age == 29


@pytest.mark.asyncio
@pytest.mark.benchmark
async def test_model_delete_performance():
    """Benchmark deleting a model from Redis."""
    user = UserModel(name="Charlie Wilson", age=40, email="charlie@example.com")
    await user.save()
    
    await user.delete()
    
    with pytest.raises(Exception):
        await UserModel.get(user.key)
