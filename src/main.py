"""Файл для запуска приложения."""

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

import chat_commands  # noqa: F401
import commands
from config import settings
from menu import (  # noqa: F401
    main_menu,
    menu_help,
    menu_setting_progile,
    menu_useful_information,
)
from menu.buttons import setting_hero_button
from migrations import db, run_connection_db
from src import Regisration, form_router
from tables.heroes_of_users import HeroesOfUsers
from tables.telegram_users import User


async def first_sms(message: Message) -> None:
    """Отправка первого сообщения после регистрации."""
    sms = """Сейчас время смены кланового задания установлено __18:30__, а первый сбор бесплатной энергии установлен на __12:00__ \\(__*по МСК*__\\)\\.

    *Если данное время неверно, то это можно с лёгкостью изменить в настройках\\!*
    Для этого нажми *Настройка профиля* \\-\\-\\-\\> *Поменять время\\.\\.\\.*

    *Так же можно __бесплатно__ подписаться на напоминалки\\!*
    Чтобы это сделать проходим *Настройка профиля* \\-\\-\\-\\> *Подписки\\.\\.\\.*"""
    await message.answer(text=sms, parse_mode=ParseMode.MARKDOWN_V2)


@form_router.callback_query(Regisration.name, F.data == "yes")
async def missing_name(call: CallbackQuery, state: FSMContext) -> None:
    """Подтверждение и сохранение никнейма героя."""
    state_data = await state.get_data()
    if "hero_id" in state_data:
        hero = await HeroesOfUsers.get(id=int(state_data["hero_id"]))  # noqa: WPS529
        await hero.update(name=state_data["name"]).apply()
    else:
        await HeroesOfUsers(
            user_id=state_data["user_id"],
            name=state_data["name"],
        ).create()
    await state.clear()
    await call.message.delete()
    await setting_hero_button(
        call.message, state_data["user_id"], "Отлично, будем знакомы)"
    )
    try:
        await first_sms(call.message)
    except Exception as err:
        logging.error(err)
        logging.info(f"Пользователь с id = {call.from_user.id}")


@form_router.callback_query(Regisration.name, F.data == "no")
async def missing_name(call: CallbackQuery) -> None:  # noqa: F811 WPS440
    """Отказ от регистрации героя/не корректно введён никнейм."""
    await call.message.delete()
    await call.message.answer(
        "Ок, давай попробуем снова. Какой у тебя ник в игре?"
    )


@form_router.message(Regisration.name)
async def reg_start(message: Message, state: FSMContext) -> None:
    """Начало регистрации героя пользователя."""
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


async def get_heroes_from_user_id(user_id: int) -> list[HeroesOfUsers]:
    """Получаем героев по id пользователя."""
    return (
        await HeroesOfUsers.join(User, HeroesOfUsers.user_id == User.id)  # noqa: WPS221
        .select()
        .where(User.user_id == user_id)
        .with_only_columns(HeroesOfUsers)
        .gino.all()
    )


# TODO @form_router.callback_query("print" in F.data)
async def choice_hero_print_rock(call: CallbackQuery) -> None:
    """Выбираем героя и выводим количество его камней."""
    await main_menu.print_rock(
        call.message, await HeroesOfUsers.get(id=int(call.data.split("-")[1]))
    )


# TODO @form_router.callback_query("add_rock" in F.data)
async def choice_hero_add_rock(call: CallbackQuery) -> None:
    """Подтверждаем выбор героя и добавляем ему камни."""
    await add_rock(
        call.message,
        int(call.data.split("-")[1]),
        await HeroesOfUsers.get(id=int(call.data.split("-")[2])),
    )


async def add_rock(
    message: Message, upg_rock: int, hero: HeroesOfUsers
) -> None:
    """Добавление камней."""
    if hero.rock == settings.MAX_COUNT_ROCKS:
        await message.answer("Да-да, я помню... Поздравляю!")
        return
    if hero.rock < upg_rock:
        await db.status(
            db.text(
                "UPDATE heroes_of_users SET rock = :upg_rock WHERE id = :hero_id;"
            ),
            {"upg_rock": upg_rock, "hero_id": hero.id},
        )
        await message.answer(
            f"Ок, я внес изменения. Тебе осталось добить {settings.MAX_COUNT_ROCKS - upg_rock}"
        )
        return
    await message.answer(
        f"Ты меня не обманешь! В прошлый раз ты писал {hero.rock}"
    )


async def set_default_commands(bot: Bot) -> None:
    """Установка команд по умолчанию."""
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Запустить бота"),
            BotCommand(command="help", description="Помощь"),
            # BotCommand(command="edit_name", description=""), # noqa: E800
            # BotCommand(command="clan_tasks", description=""), # noqa: E800
            # BotCommand(command="manul_kv", description=""), # noqa: E800
            # BotCommand(command="manul_ap_kv", description=""), # noqa: E800
            # BotCommand(command="heroes_for_events", description=""), # noqa: E800
            # BotCommand(command="pak_and_counterpak", description=""), # noqa: E800
            # BotCommand(command="useful_links", description=""), # noqa: E800
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


async def start_add_rock(message: Message, state: FSMContext) -> None:
    """Перед началом добавления камней, проверяем на количество героев и действуем по схеме."""
    heroes = await get_heroes_from_user_id(message.from_user.id)
    keyboard = []
    if not heroes:
        await commands.regisration(message, message.from_user.id, state)
    elif len(heroes) == 1:
        await add_rock(message, int(message.text), heroes[0])
    else:
        for hero in heroes:
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


@form_router.message()
async def handle_text(message: Message, state: FSMContext) -> None:
    """Обработка текста, сюда приходит все что не отсеялось ранее."""
    if message.chat.type == "private" and message.text.isnumeric():
        if 0 <= int(message.text) <= settings.MAX_COUNT_ROCKS:
            await start_add_rock(message, state)
        else:
            await message.answer(
                f"Ты меня не обманешь! У тебя не может быть больше {settings.MAX_COUNT_ROCKS} камней."
            )


async def main() -> None:
    """Initialize Bot instance with a default parse mode which will be passed to all API calls."""
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
