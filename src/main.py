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
    Message,
)

import chat_commands
import commands
from config import settings
from menu import (
    main_menu,
    menu_help,
    menu_setting_progile,
    menu_useful_information,
)
from menu.buttons import setting_hero_button
from migrations import run_connection_db
from src import Regisration, form_router
from tables.heroes_of_users import HeroesOfUsers
from tables.telegram_users import User


async def first_sms(message: Message):
    sms = """Сейчас время смены кланового задания установлено __18:30__, а первый сбор бесплатной энергии установлен на __12:00__ \(__*по МСК*__\)\.

    *Если данное время неверно, то это можно с лёгкостью изменить в настройках\!*
    Для этого нажми *Настройка профиля* \-\-\-\> *Поменять время\.\.\.*

    *Так же можно __бесплатно__ подписаться на напоминалки\!*
    Чтобы это сделать проходим *Настройка профиля* \-\-\-\> *Подписки\.\.\.*
    """
    await message.answer(sms, parse_mode=ParseMode.MARKDOWN_V2)


@form_router.callback_query(Regisration.name, F.data == "yes")
async def missing_name(call: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    if "hero_id" in data:
        hero = await HeroesOfUsers.query.where(
            HeroesOfUsers.id == data["hero_id"]
        ).gino.first()
        await hero.update(name=data["name"]).apply()
    else:
        await HeroesOfUsers(
            user_id=data["user_id"],
            name=data["name"],
        ).create()
    await state.clear()
    await call.message.delete()
    await setting_hero_button(
        call.message, data["user_id"], "Отлично, будем знакомы)"
    )
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


@form_router.callback_query("add_rock" in F.data)
async def choice_hero(call: CallbackQuery) -> None:
    hero: HeroesOfUsers = await HeroesOfUsers.query.where(
        HeroesOfUsers.id == call.data.split("-")[2]
    ).gino.first()
    await add_rock(call.message, int(call.data.split("-")[1]), hero)


async def add_rock(
    message: Message, upg_rock: int, hero: HeroesOfUsers
) -> None:
    """Добавление камней"""
    if hero.rock < upg_rock:
        await hero.update(rock=upg_rock).apply()
        await message.answer(
            f"Ок, я внес изменения. Тебе осталось добить {600 - upg_rock}"
        )
        return
    elif hero.rock == 600:
        await message.answer(f"Да-да, я помню... Поздравляю!")
        return
    await message.answer(
        f"Ты меня не обманешь! В прошлый раз ты писал {hero.rock}"
    )


async def set_default_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Запустить бота"),
            BotCommand(command="help", description="Помощь"),
            # BotCommand(command="edit_name", description=""),
            # BotCommand(command="clan_tasks", description=""),
            # BotCommand(command="manul_kv", description=""),
            # BotCommand(command="manul_ap_kv", description=""),
            # BotCommand(command="heroes_for_events", description=""),
            # BotCommand(command="pak_and_counterpak", description=""),
            # BotCommand(command="useful_links", description=""),
            BotCommand(
                command="commands_for_chat", description="Команды для чата"
            ),
            BotCommand(
                command="stop",
                description="Остановить деятельность бота (для чата)",
            ),
            BotCommand(
                command="update_time_change_clan_task",
                description="Сменить время обнуления камней.",
            ),
            BotCommand(
                command="start_remind",
                description="Активация напоминания об обнулении камней.",
            ),
            BotCommand(
                command="stop_remind",
                description="Деактивация напоминания об обнулении камней.",
            ),
            BotCommand(
                command="cancel",
                description="Отменить текущее действие и начать все с начала",
            ),
        ]
    )


@form_router.message()
async def handle_text(message: Message) -> None:
    if message.chat.type == "private" and message.text.isnumeric():
        if 0 <= int(message.text) <= 600:
            heros: list[HeroesOfUsers] = (
                await HeroesOfUsers.join(
                    User, HeroesOfUsers.user_id == User.id
                )
                .select()
                .where(User.user_id == message.from_user.id)
                .with_only_columns(HeroesOfUsers)
                .gino.all()
            )
            keyboard = []
            if len(heros) == 1:
                await add_rock(message, int(message.text), heros[0])
            else:
                for hero in heros:
                    keyboard.append(
                        [
                            InlineKeyboardButton(
                                text=hero.name,
                                callback_data=f"add_rock-{message.text}-{hero.id}",
                            )
                        ]
                    )
                await message.reply(
                    text="Кому добавим камни?",
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=keyboard
                    ),
                )
        else:
            await message.reply(
                "Ты что, хочешь меня обмануть? Проверь сколько у тебя камней!",
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
