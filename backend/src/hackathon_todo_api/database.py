from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import settings

# Async engine for FastAPI application (using asyncpg driver)
import re
from sqlalchemy.dialects.postgresql import asyncpg

# Create the async database URL by replacing the protocol
async_db_url = settings.DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://', 1)

# Remove both channel_binding and sslmode from the connection string as asyncpg handles SSL differently
async_db_url = re.sub(r'[?&]sslmode=[^&]*', '', async_db_url)
async_db_url = re.sub(r'[?&]channel_binding=[^&]*', '', async_db_url)

# Clean up URL if parameters were removed from the beginning
async_db_url = async_db_url.replace('?&', '?')
if async_db_url.endswith('?') or async_db_url.endswith('&'):
    async_db_url = async_db_url.rstrip('?&')

async_engine = create_async_engine(async_db_url)

# Sync engine for Alembic migrations (using psycopg2 driver)
from sqlalchemy import create_engine
sync_engine = create_engine(settings.DATABASE_URL)

# Async session maker
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session