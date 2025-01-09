"""Модуль с фикстурами."""

import asyncio
from asyncio import BaseEventLoop
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from _pytest.monkeypatch import MonkeyPatch
from aiogram.types import Message
from alembic.command import upgrade
from alembic.config import Config

from config import settings
from migrations import run_connection_db
from tests.factories import ClanFactory, HeroFactory, UserFactory
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
        alembic_config = Config(file_=settings.BASE_DIR + "/alembic.ini")
        alembic_config.set_main_option("sqlalchemy.url", tmp_url)
        upgrade(alembic_config, "head")

        yield tmp_url


@pytest.fixture(scope="session")
def mock_message() -> AsyncMock:
    mock_message = AsyncMock(spec=Message)
    mock_message.answer = AsyncMock()
    return mock_message


@pytest_asyncio.fixture(scope="session")
async def make_one_user_and_hero() -> tuple[UserFactory, HeroFactory]:
    """Добавляем в базу данных пользователя, его героя и клан"""
    # TODO Пока что создадим 1 пользователя и героя и 1 клан. Дальше, возможно, будем создавать циклом несколько.
    user = await UserFactory()
    return user, await HeroFactory(user_id=user.id)


@pytest_asyncio.fixture(scope="session")
async def make_clan() -> ClanFactory:
    return await ClanFactory()
