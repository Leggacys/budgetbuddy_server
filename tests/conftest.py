import pytest
import pytest_asyncio
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app import create_app
from app.database.base import Base

# Test database URL with unique DB per test
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
async def test_db():
    """Create test database for each test function"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    TestSessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    yield TestSessionLocal
    
    # Cleanup
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def test_app():
    """Create test app for each test function"""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest_asyncio.fixture(scope="function")
async def test_client(test_app):
    """Create test client for Quart app for each test function"""
    async with test_app.test_client() as client:
        yield client
