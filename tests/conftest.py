from asyncio import Task
from typing import Optional

import pytest
from httpx import AsyncClient
from yarl import URL

from app.entity import base
from alembic.command import upgrade
from app.config.settings import settings
from app.service.database import db_manager
from tests.db_utils import alembic_config_from_url, tmp_database


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio", {"use_uvloop": True}


@pytest.fixture(scope="session")
def pg_url():
    return URL(settings.DATABASE_URL)


@pytest.fixture(scope="session")
async def migrated_postgres_template(pg_url):
    async with tmp_database(pg_url, "pytest") as tmp_url:
        alembic_config = alembic_config_from_url(tmp_url)
        settings.DATABASE_URL = tmp_url

        upgrade(alembic_config, "head")
        await MIGRATION_TASK

        yield tmp_url


@pytest.fixture(scope="session")
async def sessionmanager_for_tests(migrated_postgres_template):
    db_manager.init(db_url=migrated_postgres_template)
    yield db_manager
    await db_manager.close()


@pytest.fixture()
async def session(sessionmanager_for_tests):
    async with db_manager.session() as session:
        yield session
    async with db_manager.connect() as conn:
        for table in reversed(base.Base.metadata.sorted_tables):
            await conn.execute(table.delete())
        await conn.commit()


MIGRATION_TASK: Optional[Task] = None


@pytest.fixture()
def app():
    from app.main import app

    yield app


@pytest.fixture()
async def client(session, app):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
