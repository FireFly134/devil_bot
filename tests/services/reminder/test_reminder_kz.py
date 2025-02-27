from datetime import datetime
from unittest.mock import patch

import pytest
from pytz import timezone

from services.reminder.reminder_kz import (
    description_new_kz,
    description_new_kz_in_chat_clans,
    reminder_change_kz_in_chat_clans,
    reminder_private_change_kz,
)
from tables.clans import Clans
from tables.heroes_of_users import HeroesOfUsers
from tests.factories import ClanFactory, HeroFactory, UserFactory

tz = timezone("Europe/Moscow")


@pytest.mark.parametrize(
    "count_remind, count_not_remind, count_not_subscription",
    ([0, 1, 1], [4, 5, 2], [3, 0, 2], [10, 5, 1], [0, 0, 1]),
)
@pytest.mark.asyncio()
async def test_reminder_private(
    count_remind: int, count_not_remind: int, count_not_subscription: int
) -> None:
    """Тестирование функции напоминалки в личку о смене КЗ."""
    user = await UserFactory()
    time = datetime.now(tz=tz)

    for _ in range(count_remind):
        await HeroFactory(
            user_id=user.id,
            subscription_rock=True,
            description_of_the_kz=True,
            time_change_kz=int(time.strftime("%H")),
        )
    for _ in range(count_not_remind):
        await HeroFactory(
            user_id=user.id,
            subscription_rock=True,
            description_of_the_kz=True,
            time_change_kz=int(time.strftime("%H")) + 1,
        )
    for _ in range(count_not_subscription):
        await HeroFactory(
            user_id=user.id,
            subscription_rock=False,
            description_of_the_kz=False,
            time_change_kz=int(time.strftime("%H")),
        )
    heroes = await HeroesOfUsers.query.gino.all()
    assert (
        len(heroes) == count_remind + count_not_remind + count_not_subscription
    )

    with patch(
        "services.reminder.reminder_kz.send_msg",
    ) as mock_send_msg:
        await reminder_private_change_kz(time)
        assert mock_send_msg.call_count == count_remind

    with patch(
        "services.reminder.reminder_kz.send_msg_mv2",
    ) as mock_send_msg_mv2:
        await description_new_kz(time)
        assert mock_send_msg_mv2.call_count == count_remind


@pytest.mark.parametrize(
    "count_remind, count_not_remind, count_not_subscription, clan_stop",
    ([0, 1, 1, 0], [4, 5, 2, 1], [3, 0, 2, 1], [10, 5, 1, 0], [0, 0, 1, 2]),
)
@pytest.mark.asyncio()
async def test_reminder_groups(
    count_remind: int,
    count_not_remind: int,
    count_not_subscription: int,
    clan_stop: int,
) -> None:
    """Тестирование функции напоминалки в личку о смене КЗ."""
    time = datetime.now(tz=tz)
    for _ in range(count_remind):
        await ClanFactory(
            start=True,
            subscription_rock=True,
            description_of_the_kz=True,
            time_kz=int(time.strftime("%H")),
        )
    for _ in range(count_not_remind):
        await ClanFactory(
            start=True,
            subscription_rock=True,
            description_of_the_kz=True,
            time_kz=int(time.strftime("%H")) + 1,
        )
    for _ in range(count_not_subscription):
        await ClanFactory(
            start=True,
            subscription_rock=False,
            description_of_the_kz=False,
            time_kz=int(time.strftime("%H")),
        )
    for _ in range(clan_stop):
        await ClanFactory(
            start=False,
            subscription_rock=True,
            description_of_the_kz=True,
            time_kz=int(time.strftime("%H")),
        )
    clans = await Clans.query.gino.all()
    assert (
        len(clans)
        == count_remind + count_not_remind + count_not_subscription + clan_stop
    )
    with patch(
        "services.reminder.reminder_kz.send_msg",
    ) as mock_send_msg:
        await reminder_change_kz_in_chat_clans(time)
        assert mock_send_msg.call_count == count_remind

    with patch(
        "services.reminder.reminder_kz.send_msg_mv2",
    ) as mock_send_msg_mv2:
        await description_new_kz_in_chat_clans(time)
        assert mock_send_msg_mv2.call_count == count_remind
