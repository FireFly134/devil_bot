from datetime import datetime

from config import settings
from tables.statistics import Statistics
from tables.telegram_users import User


def statistics(text: str | None = None, is_state: bool = False):
    """Декоратор для обновления времени update_at у пользователя.
    На выходе в функцию отдает func(message, state)"""

    def decorator(func):
        async def wrapper(*args, **kwargs):
            if settings.TESTING:
                return await func(*args)
            user = await User.query.where(
                User.user_id == kwargs.get("event_from_user").id
            ).gino.first()
            if user:
                await user.update(update_at=datetime.now()).apply()
            if text:
                await Statistics(
                    user_id=user.id if user else None,
                    tg_user_id=kwargs.get("event_from_user").id,
                    action=text,
                ).create()
            if is_state:
                return await func(*args, kwargs.get("state"))
            return await func(*args)

        return wrapper

    return decorator
