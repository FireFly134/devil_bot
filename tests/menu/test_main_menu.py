from unittest.mock import AsyncMock

import pytest

from config import settings
from menu.main_menu import print_rock
from tables.heroes_of_users import HeroesOfUsers


def get_check_data_for_print_rock():
    return [
        (rock, get_answer(rock))
        for rock in (0, 200, 400, settings.MAX_COUNT_ROCKS)
    ]


def get_answer(rock: int) -> str:
    if rock == 0:
        return "Ты еще не вводил количество своих камней. Введи количество цифрами!"
    return (
        f'У твоего героя под ником "Test Hero" - "{rock}" камней! '
        f"Осталось добить {settings.MAX_COUNT_ROCKS - rock}. "
        f"До обновления К.З. осталось"
    )


@pytest.mark.parametrize(("rock", "answer"), get_check_data_for_print_rock())
@pytest.mark.asyncio()
async def test_print_rock(
    rock: int, answer: str, mock_message: AsyncMock
) -> None:
    """Тестирование функции отображение количества камней (print_rock)."""
    mock_hero = AsyncMock(spec=HeroesOfUsers)
    mock_hero.time_change_kz = 18
    mock_hero.rock = rock
    mock_hero.name = "Test Hero"
    # Вызываем тестируемую функцию
    await print_rock(mock_message, mock_hero)

    assert mock_message.answer.called
    # Проверяем, что метод answer был вызван с ожидаемыми аргументами
    assert answer in mock_message.answer.await_args[0][0]
