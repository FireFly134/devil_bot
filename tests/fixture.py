"""Модуль с фикстурами."""

import asyncio
from asyncio import BaseEventLoop

import pytest
from _pytest.monkeypatch import MonkeyPatch
from alembic.command import upgrade
from alembic.config import Config

from migrations import run_connection_db

from tests.utils import get_tmp_database


@pytest.fixture(scope="session")
def loop() -> BaseEventLoop:
    """Получить цикл событий."""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def monkeypatch_session() -> MonkeyPatch:
    """Инициализация monkeypatch."""
    patch = MonkeyPatch()
    yield patch
    patch.undo()


@pytest.fixture(autouse=True)
async def db(monkeypatch_session: MonkeyPatch) -> str:
    """Инициализация подключения к бд."""
    with get_tmp_database() as tmp_url:
        alembic_config = Config(file_='.././alembic.ini')
        alembic_config.set_main_option("sqlalchemy.url", tmp_url)
        upgrade(alembic_config, "head")

        yield tmp_url


@pytest.fixture(autouse=True)
async def init_db(monkeypatch_session: MonkeyPatch) -> None:
    """Инициализация подключения к бд."""
    await run_connection_db()