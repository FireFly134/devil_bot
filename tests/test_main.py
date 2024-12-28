from unittest.mock import AsyncMock

import pytest
from aiogram.enums import ParseMode
from aiogram.types import Message
from factories import HeroFactory, UserFactory

from main import first_sms, get_hero_from_hero_id, get_heroes_from_user_id


@pytest.mark.asyncio
async def test_get_hero() -> None:
    user = await UserFactory()
    hero = await HeroFactory(user_id=user.id)
    for check_hero in await get_heroes_from_user_id(user.user_id):
        assert hero.id == check_hero.id
        assert hero.name == check_hero.name
    check_hero = await get_hero_from_hero_id(hero.id)
    assert hero.id == check_hero.id
    assert hero.name == check_hero.name


@pytest.mark.asyncio
async def test_first_sms():
    """Тестирование функции first_sms."""
    mock_message = AsyncMock(spec=Message)
    mock_message.answer = AsyncMock()

    # Вызываем тестируемую функцию
    await first_sms(mock_message)

    assert mock_message.answer.called
    # Проверяем, что метод answer был вызван с ожидаемыми аргументами
    assert (
        mock_message.answer.await_args[1]["text"]
        == "Сейчас время смены кланового задания установлено __18:30__, а первый сбор бесплатной энергии установлен на __12:00__ \\(__*по МСК*__\\)\\.\n\n    *Если данное время неверно, то это можно с лёгкостью изменить в настройках\\!*\n    Для этого нажми *Настройка профиля* \\-\\-\\-\\> *Поменять время\\.\\.\\.*\n\n    *Так же можно __бесплатно__ подписаться на напоминалки\\!*\n    Чтобы это сделать проходим *Настройка профиля* \\-\\-\\-\\> *Подписки\\.\\.\\.*\n    "
    )
    assert (
        mock_message.answer.await_args[1]["parse_mode"]
        == ParseMode.MARKDOWN_V2
    )
