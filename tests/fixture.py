"""Модуль с фикстурами."""

import asyncio
from asyncio import BaseEventLoop

import pytest
import pytest_asyncio
from _pytest.monkeypatch import MonkeyPatch
from alembic.command import upgrade
from alembic.config import Config

from migrations import run_connection_db

from tests.utils import get_tmp_database


@pytest.fixture(autouse=True)
def loop() -> BaseEventLoop:
    """Получить цикл событий."""
    with open("tmp_db_url.txt", "a+") as f:
        f.writelines(" start_fixture_loop")
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def monkeypatch_session() -> MonkeyPatch:
    """Инициализация monkeypatch."""
    with open("tmp_db_url.txt", "a+") as f:
        f.writelines(" start_fixture_monkeypatch_session")
    patch = MonkeyPatch()
    yield patch
    with open("tmp_db_url.txt", "a+") as f:
        f.writelines("stop_fixture_monkeypatch_session")
    patch.undo()


@pytest_asyncio.fixture(autouse=True)
async def run_connection(db: str, monkeypatch_session: MonkeyPatch) -> None:
    """Инициализация приложения."""
    await run_connection_db()


@pytest.fixture()
def db(monkeypatch_session: MonkeyPatch) -> str:
    """Инициализация подключения к бд."""
    with get_tmp_database() as tmp_url:
        alembic_config = Config(file_='.././alembic.ini')
        alembic_config.set_main_option("sqlalchemy.url", tmp_url)
        upgrade(alembic_config, "head")

        yield tmp_url
