# database.py

from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from asyncio import current_task
from config import config

# Connect FastAPI with SQLAlchemy
db_url=f"postgresql+asyncpg://{config.db_user}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_name}"
engine = create_async_engine(db_url)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
async_session = scoped_session(async_session_factory, scopefunc=current_task)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        
async def recreate_db(Base):
    # Drop and recreate tables to ensure a clean slate
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)