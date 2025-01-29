from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from services.reminder.reminder_events import reminder_events
from tests.factories import UserFactory, EventFactory


@pytest.mark.asyncio()
async def test_reminder_events() -> None:
    """Тестирование функции напоминания о сборе энергии."""
    time = datetime.now()
    await UserFactory(subscription_event=True)
    await EventFactory(event_date=(time+timedelta(days=2)).date())

    with patch(
        "services.reminder.reminder_events.send_msg_mv2",
    ) as mock_send_msg:
        await reminder_events()
        assert mock_send_msg.call_count == 1
