"""Модуль с фабриками."""
from datetime import datetime
from typing import Coroutine

import factory
from gino.declarative import ModelType

from src.tables.clans import Clans
from src.tables.heroes_of_users import HeroesOfUsers
from src.tables.telegram_users import User
from tables.events import Events


class BaseFactory(factory.Factory):
    """Базовый класс фабрики."""

    @classmethod
    def _create(
        cls,
        model_class: ModelType,
        *args: tuple,
        **kwargs: dict,
    ) -> Coroutine:
        """Модифицированный метод создания записи в бд под gino."""

        async def create_coro(*args: tuple, **kwargs: dict) -> Coroutine:
            return await model_class.create(*args, **kwargs)

        return create_coro(*args, **kwargs)


class UserFactory(BaseFactory):
    """Фабрика пользователя."""

    class Meta:
        """Метакласс с настройками."""

        model = User

    user_id = factory.Sequence(lambda n: n)
    first_name = factory.Sequence(lambda n: f"Test{n}")
    last_name = factory.Sequence(lambda n: f"tseT{n}")
    username = factory.Sequence(lambda n: f"TseT{n}")
    language_code = "ru"
    send_msg = True


class HeroFactory(BaseFactory):
    """Фабрика героя пользователя."""

    class Meta:
        """Метакласс с настройками."""

        model = HeroesOfUsers

    user_id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f"Test{n}")
    rock = 0


class ClanFactory(BaseFactory):
    """Фабрика клана."""

    class Meta:
        """Метакласс с настройками."""

        model = Clans

    name_clan = factory.Sequence(lambda n: f"TestClan{n}")
    chat_id = factory.Sequence(lambda n: f"-{n}")


class EventFactory(BaseFactory):
    """Фабрика событий."""

    class Meta:
        """Метакласс с настройками."""

        model = Events

    name_event = factory.Sequence(lambda n: f"TestEvent{n}")
    event_date = factory.Sequence(lambda n: datetime.now().date())
    description = factory.Sequence(lambda n: f"Test_Description_{n}")
