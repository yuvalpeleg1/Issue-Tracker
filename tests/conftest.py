"""
Shared fixtures for API tests.

Key idea: FastAPI's TestClient talks to your app in-process — no need for
uvicorn or the Vite server. We still hit the same routes the React app uses
via /api/v1/issues/.

Tests use an in-memory SQLite database so they never touch Postgres.
"""

import asyncio
from collections.abc import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
import app.models  # noqa: F401 — register Issue on Base.metadata
from main import app

TEST_DATABASE_URL = "sqlite+aiosqlite://"


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Override get_db with an isolated in-memory SQLite session."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def init_models() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(init_models())

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    asyncio.run(engine.dispose())
