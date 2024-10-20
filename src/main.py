import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from aiogram.fsm.context import FSMContext

from aiogram.types import (
    BotCommand,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)

from buttons import setting_hero_button
from config import settings
from migrations import run_connection_db
from tables.heroes_of_users import HeroesOfUsers

from src import form_router, Regisration
import commands


async def first_sms(message: Message):
    sms = """Сейчас время смены кланового задания установлено __18:30__, а первый сбор бесплатной энергии установлен на __12:00__ \(__*по МСК*__\)\.

    *Если данное время неверно, то это можно с лёгкостью изменить в настройках\!*
    Для этого нажми *Настройка профиля* \-\-\-\> *Поменять время\.\.\.*

    *Так же можно __бесплатно__ подписаться на напоминалки\!*
    Чтобы это сделать проходим *Настройка профиля* \-\-\-\> *Подписки\.\.\.*
    """
    await message.answer(sms, parse_mode=ParseMode.MARKDOWN_V2)


# @form_router.message(CommandStart())
# async def start(message: Message, state: FSMContext) -> None:
#     if message.chat.type == "private":
#         if message.from_user is not None:
#             user_id: int = int(message.from_user.id)
#             if user := await User.query.where(
#                 User.user_id == user_id
#             ).gino.first():
#                 if hero_user_search := await HeroesOfUsers.query.where(
#                     HeroesOfUsers.user_id == user.id
#                 ).gino.first():
#                     sms = f"Привет, {str(hero_user_search.name)}"
#                     await new_button(message, sms)
#                     return
#                 # user(message, sms)
#             else:
#                 user = await User(
#                     user_id=user_id,
#                     first_name=message.from_user.first_name,
#                     last_name=message.from_user.last_name,
#                     username=message.from_user.username,
#                     language_code=message.from_user.language_code,
#                 ).create()
#                 await message.answer(
#                     "Я тебя не помню. Давай знакомиться! Какой у тебя ник в игре?"
#                 )
#             await state.update_data(user_id=user.id)
#             await state.set_state(Regisration.name)


@form_router.callback_query(Regisration.name, F.data == "yes")
async def missing_name(call: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    if "hero_id" in data:
        hero = await HeroesOfUsers.query.where(
            HeroesOfUsers.id == data["hero_id"]
        )
        hero.update(name=data["name"]).apply()
    else:
        await HeroesOfUsers(
            user_id=data["user_id"],
            name=data["name"],
        ).create()
    await state.clear()
    await call.message.delete()
    await setting_hero_button(call.message, "Отлично, будем знакомы)")
    try:
        await first_sms(call.message)
    except Exception as err:
        logging.error(err)
        logging.info(f"Пользователь с id = {call.from_user.id}")


@form_router.callback_query(Regisration.name, F.data == "no")
async def missing_name(call: CallbackQuery) -> None:
    await call.message.delete()
    await call.message.answer(
        "Ок, давай попробуем снова. Какой у тебя ник в игре?"
    )


@form_router.message(Regisration.name)
async def reg_start(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer(
        f'Ты герой под ником "{message.text}"?',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Да", callback_data="yes"),
                    InlineKeyboardButton(text="Нет", callback_data="no"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


async def set_default_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Запустить бота"),
            BotCommand(
                command="cancel",
                description="Отменить текущее действие и начать все с начала",
            ),
        ]
    )


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed
    # to all API calls
    bot = Bot(
        token=settings.TOKEN,
        session=AiohttpSession(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await run_connection_db()
    await set_default_commands(bot)
    dp = Dispatcher()
    dp.include_router(form_router)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
