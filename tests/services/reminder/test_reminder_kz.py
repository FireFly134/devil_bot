from datetime import datetime
from unittest.mock import patch

import pytest

from services.reminder.reminder_kz import reminder_kz
from tables.heroes_of_users import HeroesOfUsers
from tests.factories import HeroFactory, UserFactory


@pytest.mark.parametrize(
    "count_remind, count_not_remind, count_not_subscription",
    ([0, 1, 1], [4, 5, 2], [3, 0, 2], [10, 5, 1], [0, 0, 1]),
)
@pytest.mark.asyncio()
async def test_reminder_zero(
    count_remind, count_not_remind, count_not_subscription
) -> None:
    """Тестирование функции отображение количества камней (print_rock)."""
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
    # По дефолту start=True, remain_zero_rock=True,
    # поэтому должно быть 2 вызова на отправку сообщений из 5.
    with patch(
        "services.reminder.reminder_energy.send_msg_mv2",
    ) as mock_send_msg:
        await reminder_energy()
        assert mock_send_msg.call_count == count_remind
