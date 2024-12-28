"""Модуль с фикстурами."""

from aiogram.types import Message

import asyncio
from asyncio import BaseEventLoop
from unittest.mock import AsyncMock

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
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def monkeypatch_session() -> MonkeyPatch:
    """Инициализация monkeypatch."""
    patch = MonkeyPatch()
    yield patch
    patch.undo()


@pytest_asyncio.fixture(autouse=True)
async def run_connection(db: str, monkeypatch_session: MonkeyPatch) -> None:
    """Инициализация приложения."""
    await run_connection_db()


@pytest.fixture()
def db(monkeypatch_session: MonkeyPatch) -> str:
    """Инициализация подключения к бд."""
    with get_tmp_database() as tmp_url:
        alembic_config = Config(file_=".././alembic.ini")
        alembic_config.set_main_option("sqlalchemy.url", tmp_url)
        upgrade(alembic_config, "head")

        yield tmp_url


@pytest.fixture(scope="session")
def mock_message() -> AsyncMock:
    mock_message = AsyncMock(spec=Message)
    mock_message.answer = AsyncMock()
    return mock_message