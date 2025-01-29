from random import randint
from unittest.mock import patch

import pytest

from services.reminder.reminder_and_cleaner_rock import (
    clear_rock,
    reminder_zero,
)
from tables.heroes_of_users import HeroesOfUsers
from tests.factories import ClanFactory, HeroFactory, UserFactory


@pytest.mark.asyncio()
async def test_reminder_zero() -> None:
    """Тестирование функции отображение количества камней (print_rock)."""
    await ClanFactory()
    await ClanFactory()
    await ClanFactory(start=False)
    await ClanFactory(remain_zero_rock=False)
    await ClanFactory(start=False, remain_zero_rock=False)
    # По дефолту start=True, remain_zero_rock=True,
    # поэтому должно быть 2 вызова на отправку сообщений из 5.
    with patch(
        "services.reminder.reminder_and_cleaner_rock.send_msg",
    ) as mock_send_msg:
        await reminder_zero()
        assert mock_send_msg.call_count == 2


@pytest.mark.asyncio()
async def test_clear_rock() -> None:
    """Тестирование функции отображение количества камней (print_rock)."""
    for _ in range(5):
        user = await UserFactory()
        await HeroFactory(user_id=user.id)
    for _ in range(10):
        user = await UserFactory()
        count_rock = randint(1, 600)
        await HeroFactory(user_id=user.id, rock=count_rock)
    assert (
        len(
            await HeroesOfUsers.query.where(HeroesOfUsers.rock == 0).gino.all()
        )
        == 5
    )
    with patch(
        "services.reminder.reminder_and_cleaner_rock.reminder_zero",
    ) as mock_send_msg:
        await clear_rock()
        assert mock_send_msg.call_count == 1
    assert (
        len(
            await HeroesOfUsers.query.where(HeroesOfUsers.rock == 0).gino.all()
        )
        == 15
    )
