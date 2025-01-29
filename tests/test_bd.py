import pytest

from tests.factories import UserFactory


@pytest.mark.asyncio()
async def test_create_user():
    user = await UserFactory()
    assert user.send_msg
