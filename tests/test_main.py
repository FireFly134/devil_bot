from unittest.mock import AsyncMock

import pytest
from aiogram.enums import ParseMode
from factories import HeroFactory, UserFactory

from main import (
    add_rock,
    first_sms,
    get_hero_from_hero_id,
    get_heroes_from_user_id,
)
from tables.heroes_of_users import HeroesOfUsers


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
async def test_first_sms(mock_message: AsyncMock):
    """Тестирование функции first_sms."""
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


@pytest.mark.parametrize(
    "rock, upg_rock", [(0, 100), (200, 200), (300, 603), (4, 400), (600, 5)]
)
@pytest.mark.asyncio
async def test_add_rock(
    rock: int, upg_rock: int, mock_message: AsyncMock
) -> None:
    user = await UserFactory()
    hero = await HeroFactory(user_id=user.id, rock=rock)
    await add_rock(mock_message, upg_rock, hero)
    update_hero = await HeroesOfUsers.get(hero.id)
    if rock < upg_rock <= 600:
        assert update_hero.rock == upg_rock
    else:
        assert update_hero.rock == rock
