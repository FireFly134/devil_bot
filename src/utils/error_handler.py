"""Модуль для обработки ошибок."""
import logging
from typing import Any, Callable

from aiogram.types import Message

logger = logging.getLogger(__name__)


async def safe_execute(func: Callable, *args, **kwargs) -> Any:
    """Безопасное выполнение функции с обработкой ошибок."""
    try:
        return await func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Ошибка в функции {func.__name__}: {e}")
        return None


def handle_message_errors(func: Callable) -> Callable:
    """Декоратор для обработки ошибок в обработчиках сообщений."""

    async def wrapper(message: Message, *args, **kwargs):
        try:
            return await func(message, *args, **kwargs)
        except Exception as e:
            logger.error(
                f"Ошибка в обработчике {func.__name__} для пользователя {message.from_user.id}: {e}"
            )
            try:
                await message.answer(
                    "Произошла ошибка. Попробуйте еще раз или обратитесь к администратору."
                )
            except Exception:
                # Если не удается отправить сообщение, просто логируем
                logger.error(
                    "Не удалось отправить сообщение об ошибке пользователю"
                )

    return wrapper
