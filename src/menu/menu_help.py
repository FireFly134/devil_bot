from aiogram import F
from aiogram.enums import ParseMode
from aiogram.types import Message

from src import form_router
from src.menu.text_menu import menu_help
from tables.text_table import TextTable


async def get_text(name_text: str) -> str:
    """Получение текста из таблицы в БД"""
    text_obj = await TextTable.query.where(
        TextTable.name_text == name_text
    ).gino.first()
    return text_obj.text


@form_router.message(F.text == menu_help["instructions_for_use"])
async def instructions_for_use(message: Message) -> None:
    """Отправка инструкций по эксплуатации бота"""
    await message.answer(await get_text("Instructions_for_use"))


@form_router.message(
    F.text == menu_help["instructions_for_implementing_the_bot_in_the_chat"]
)
async def instructions_for_implementing_the_bot_in_the_chat(
    message: Message,
) -> None:
    """Отправка инструкций по эксплуатации бота в чате"""
    info = await get_text("Instructions_for_implementing_the_bot_in_the_chat")
    text = (
        info.replace(">", "\>")
        .replace("#", "\#")
        .replace("+", "\+")
        .replace("=", "\=")
        .replace("-", "\-")
        .replace("{", "\{")
        .replace("}", "\}")
        .replace(".", "\.")
        .replace("!", "\!")
    )
    await message.answer(text, parse_mode=ParseMode.MARKDOWN_V2)


@form_router.message(F.text == menu_help["basic_commands_in_the_chat"])
async def basic_commands_in_the_chat(message: Message) -> None:
    """Отправка базовых команд в чате"""
    await message.answer(await get_text("Basic_commands_in_the_chat"))
