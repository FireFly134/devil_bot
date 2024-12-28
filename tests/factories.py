"""Модуль с фабриками."""

from typing import Coroutine

import factory
from gino.declarative import ModelType

from src.tables.telegram_users import User
from tables.heroes_of_users import HeroesOfUsers


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
    """Фабрика пользователя."""

    class Meta:
        """Метакласс с настройками."""

        model = HeroesOfUsers

    user_id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f"Test{n}")
