import logging

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from config import settings


def wlog(func):
    async def wrapper(*args, **kwargs):
        bot = Bot(
            token=settings.TOKEN,
            session=AiohttpSession(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        try:
            await func(bot=bot, *args, **kwargs)
        except Exception as err:
            logging.error(err)
            logging.info(f"Пользователь (или чат) с id = {kwargs['user_id']}")
        finally:
            await bot.session.close()

    return wrapper


@wlog
async def send_msg(user_id: int | str, sms: str, bot: Bot) -> None:
    """Отправить обычное сообщение."""
    await bot.send_message(chat_id=user_id, text=sms)


@wlog
async def send_msg_mv2(user_id: int | str, sms: str, bot: Bot) -> None:
    """Отправить сообщение в формате MarkdownV2."""
    await bot.send_message(
        chat_id=user_id, text=sms, parse_mode=ParseMode.MARKDOWN_V2
    )
