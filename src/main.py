import asyncio
import os
from typing import Any

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.types import FSInputFile

from config import settings
from tables.heroes_of_users import HeroesOfUsers
from tables.telegram_users import User

dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message) -> None:
    # user_id = message.from_user.id
    await message.answer("Привет, меня зовут Люцик!")


async def set_default_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            types.BotCommand(command="start", description="Запустить бота"),
            types.BotCommand(
                command="cancel",
                description="Отменить текущее действие и начать все с начала",
            ),
        ]
    )
    return


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed
    # to all API calls
    bot = Bot(token=settings.TOKEN, session=AiohttpSession())
    # bot = Bot(settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await set_default_commands(bot)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
