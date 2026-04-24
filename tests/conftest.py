import os
from pathlib import Path

import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

TEST_DB_FILE = Path("test_app.db")
TEST_DATABASE_URL = f"sqlite+aiosqlite:///./{TEST_DB_FILE.name}"

os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from src.main import app
from src.core.database import get_db_session

engine_test = create_async_engine(TEST_DATABASE_URL, future=True)
TestingSessionLocal = async_sessionmaker(
    bind=engine_test,
    expire_on_commit=False,
    class_=AsyncSession,
)


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    if TEST_DB_FILE.exists():
        TEST_DB_FILE.unlink()

    run_migrations()

    yield

    if TEST_DB_FILE.exists():
        TEST_DB_FILE.unlink()


@pytest_asyncio.fixture
async def clean_db():
    async with engine_test.begin() as conn:
        await conn.execute(text("DELETE FROM transactions"))
        await conn.execute(text("DELETE FROM accounts"))
        await conn.execute(text("DELETE FROM users"))
        await conn.commit()
    yield


@pytest_asyncio.fixture
async def db_session(clean_db):
    async with TestingSessionLocal() as session:
        yield session


async def override_get_db_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def client(clean_db):
    app.dependency_overrides[get_db_session] = override_get_db_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    yield engine_test
    await engine_test.dispose()
