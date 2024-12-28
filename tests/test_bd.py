import pytest

from tables.telegram_users import User

from tests.factories import UserFactory

@pytest.mark.asyncio
async def test_create_user():
    user = await UserFactory()
    assert user.send_msg


@pytest.mark.asyncio
async def test_read_user():
    # Создаем тестовые данные
    await User.create(name="Alice")
    await User.create(name="Bob")

    # Читаем
    users = await User.query.gino.all()
    assert len(users) == 2
    assert users[0].name == "Alice"
    assert users[1].name == "Bob"
