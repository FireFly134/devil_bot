from unittest.mock import AsyncMock

import pytest
from _pytest.monkeypatch import MonkeyPatch
import commands
import chat_commands
from commands import start, helper, regisration
from tests.factories import UserFactory, HeroFactory


@pytest.mark.asyncio
@pytest.mark.parametrize("chat_type, is_registered", [
    # ("private", True),
    ("private", False),
    ("group", True),
    ("group", False),
])
async def test_start(chat_type: str, is_registered: bool, monkeypatch: MonkeyPatch, mock_message: AsyncMock, mock_state: AsyncMock) -> None:
    """Test start command."""
    if chat_type != "private":
        mock_message.chat.type = chat_type
        mock_chat_start = AsyncMock()
        monkeypatch.setattr(commands, "chat_start", mock_chat_start)
    result = ""
    if is_registered:
        user = await UserFactory(user_id=mock_message.from_user.id)
        hero = await HeroFactory(user_id=user.id)
        result = f"Привет, {hero.name}"
    else:
        mock_regisration = AsyncMock()
        monkeypatch.setattr(commands, "regisration", mock_regisration)
    await start(mock_message, mock_state)
    if is_registered and chat_type == "private":
        assert mock_message.answer.call_count == 1
        assert result == mock_message.answer.await_args[0][0]
    else:
        assert mock_message.answer.call_count == 0

async def test_helper(mock_message: AsyncMock) -> None:
    """Test start command."""
    ...

async def test_regisration(mock_message: AsyncMock) -> None:
    """Test start command."""
    ...

