import pytest
from starlette.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import sys
import os
from main import app
from database import get_db

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def pytest_html_report_title(report):  
    report.title = "Pytest HTML Report for SasS Family Budget Tracker FASTAPI application"

@pytest.fixture(scope="module")
def test_app():
    """
    Fixture that provides a TestClient instance for testing the FastAPI application.
    Yields:
        TestClient: An instance of TestClient initialized with the FastAPI app.
    """

    client = TestClient(app)
    yield client

@pytest.fixture(scope="module")
async def override_get_db():
    """
    Asynchronous generator function that provides a database session for testing purposes.
    Yields:
        AsyncSession: An instance of the test database session.
    Commits the session if no exceptions occur; otherwise, rolls back the session and re-raises the exception.
    Intended to be used as a dependency override in tests.
    """

    async with TestSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
@pytest.fixture(scope="module")
async def override_recreate_db(Base):
    """
    Overrides the application's database dependency to recreate the database schema for testing.
    This function drops all tables and recreates them using the provided SQLAlchemy Base metadata.
    It is intended to be used as a fixture in tests to ensure a clean database state before each test run.
    Args:
        Base: The SQLAlchemy declarative base containing the metadata for the database schema.
    Yields:
        None. This is a generator function used for setup and teardown in test fixtures.
    """
        
    async def _recreate():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            return _recreate
    app.dependency_overrides[get_db] = _recreate
    yield
    app.dependency_overrides = {}

