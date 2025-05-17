import sys
import os
# Ensure the project root is in sys.path for module resolution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker
from main import app
from database import get_db

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session")
def anyio_backend():
    return 'asyncio'

@pytest.fixture(scope="session")
def test_app():
    """
    Fixture that provides a TestClient instance for testing the FastAPI application.
    """
    return TestClient(app)

@pytest.fixture(scope="function")
async def override_get_db():
    """
    Override get_db dependency to use the test SQLite database.
    Yields:
        AsyncSession: An instance of the test database session.
    """
    async with TestSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise

# Apply the override before each test
@pytest.fixture(autouse=True, scope="function")
def apply_db_override(override_get_db):
    app.dependency_overrides[get_db] = lambda: override_get_db
    yield
    app.dependency_overrides = {}

@pytest.fixture(scope="session", autouse=True)
async def create_test_db():
    """
    Create the database schema for testing before any tests run.
    """
    from models.base import Base
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Optionally, drop tables after tests
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
