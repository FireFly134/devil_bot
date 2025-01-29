from datetime import datetime
from unittest.mock import patch

import pytest

from services.reminder.reminder_energy import reminder_energy
from tables.heroes_of_users import HeroesOfUsers
from tests.factories import HeroFactory, UserFactory


@pytest.mark.parametrize(
    "count_remind, count_not_remind, count_not_subscription",
    ([0, 1, 1], [4, 5, 2], [3, 0, 2], [10, 5, 1], [0, 0, 1]),
)
@pytest.mark.asyncio()
async def test_reminder_energy(
    count_remind: int, count_not_remind: int, count_not_subscription: int
) -> None:
    """Тестирование функции напоминания о сборе энергии."""
    time = datetime.now()
    user = await UserFactory()
    for _ in range(count_remind):
        await HeroFactory(
            user_id=user.id,
            subscription_energy=True,
            time_collection_energy=int(time.strftime("%H")),
        )
    for _ in range(count_not_remind):
        await HeroFactory(
            user_id=user.id,
            subscription_energy=True,
            time_collection_energy=int(time.strftime("%H")) + 1,
        )
    for _ in range(count_not_subscription):
        await HeroFactory(
            user_id=user.id,
            subscription_energy=False,
            time_collection_energy=int(time.strftime("%H")),
        )
    heroes = await HeroesOfUsers.query.gino.all()
    assert (
        len(heroes) == count_remind + count_not_remind + count_not_subscription
    )
    with patch(
        "services.reminder.reminder_energy.send_msg_mv2",
    ) as mock_send_msg:
        await reminder_energy()
        assert mock_send_msg.call_count == count_remind
