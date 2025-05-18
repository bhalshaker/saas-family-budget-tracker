import sys
import os
# Ensure the project root is in sys.path for module resolution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker
from main import app
from database import get_db
from datetime import datetime
from models import Base

# Use SQLite for testing (async, in-memory)
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def anyio_backend():
    return 'asyncio'

@pytest.fixture(autouse=True, scope="function")
def apply_db_override():
    async def _override_get_db():
        async with TestSessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides = {}

@pytest.fixture(autouse=True,scope="function")
async def create_test_db():
    """
    Create the database schema for testing before any tests run.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield