from unittest.mock import AsyncMock

from aiogram.fsm.context import FSMContext

from src.menu.menu_setting_progile import show_data_profile

import pytest

from tests.factories import UserFactory, HeroFactory, ClanFactory


def get_profile_data(name) -> str:
    return (f"Ваш ник в игре: {name}\n"
            "❗️ Вы не подписаны на оповещение по камням.\n"
            "❗️ Вы не подписаны на оповещение по сбору энергии.\n"
            "❗️ Вы не подписаны на ежедневное описание КЗ.\n"
            "Время смены КЗ: 18:30 по мск \n"
            "Время сбора первой энергии: 12:00 по мск\n")


@pytest.mark.asyncio
@pytest.mark.parametrize("is_clan", [True, False])
async def test_show_data_profile(is_clan, mock_message: AsyncMock) -> None:
    """Тестирование функции отображение данных о профиле."""
    user = await UserFactory()
    await HeroFactory(user_id=user.id)
    hero = await HeroFactory(user_id=user.id)
    await HeroFactory(user_id=user.id)
    result = get_profile_data(hero.name)
    if is_clan:
        clan = await ClanFactory()
        await hero.update(clan_id=clan.id).apply()
        result+=f'Вы в клане "{clan.name_clan}"'
    state = AsyncMock(spec=FSMContext)
    state.get_data = AsyncMock(
        return_value={
            "user_id": user.id,
            "hero_id": hero.id,
        }
    )
    await show_data_profile(mock_message, state)
    assert mock_message.answer.called == 1
    # Проверяем, что метод answer был вызван с ожидаемыми аргументами
    assert result == mock_message.answer.await_args[0][0]


