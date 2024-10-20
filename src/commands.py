from aiogram.exceptions import TelegramBadRequest

from src import form_router, Regisration

from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
)

from buttons import new_button
from tables.clans import Clans

from tables.heroes_of_users import HeroesOfUsers
from tables.telegram_users import User

@form_router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    if message.chat.type == "private":
        if message.from_user is not None:
            user_id: int = int(message.from_user.id)
            if user := await User.query.where(
                User.user_id == user_id
            ).gino.first():
                if hero_user_search := await HeroesOfUsers.query.where(
                    HeroesOfUsers.user_id == user.id
                ).gino.first():
                    sms = f"Привет, {str(hero_user_search.name)}"
                    await new_button(message, sms)
                    return
                # user(message, sms)
            else:
                user = await User(
                    user_id=user_id,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name,
                    username=message.from_user.username,
                    language_code=message.from_user.language_code,
                ).create()
                await message.answer(
                    "Я тебя не помню. Давай знакомиться! Какой у тебя ник в игре?"
                )
            await state.update_data(user_id=user.id)
            await state.set_state(Regisration.name)
    else:
        chat_id: str = str(message.chat.id)
        if clan := await Clans.query.where(
                Clans.chat_id == chat_id
        ).gino.first():
            if clan.start:
                await message.answer(f"Привет, {clan.name_clan}!",
                )
            else:
                await clan.update(start=True).apply()
                await message.answer(f"Привет, {clan.name_clan}!\nЯ снова с вами!😈",
                )
        else:
            await Clans(
                chat_id=chat_id,
                name_clan=message.chat.title,
            ).create()
            await message.answer("Привет, меня зовут Люцик!"
            )


@form_router.message(Command('stop'))
async def stop(message: Message) -> None:
    if message.chat.type != "private":
        chat_id: str = str(message.chat.id)
        if clan := await Clans.query.where(
            Clans.chat_id == chat_id
        ).gino.first():
            if clan.start:
                await clan.update(start = False).apply()
                await message.answer("Ок, я все понял!☹️\nЯ пошел...")
                return
        await message.answer("А что я? Я молчу!☹️")



async def remind(message: Message, remain_zero_rock: bool) -> None:
    """Активация/деактивация напоминания об обнуление камней."""
    if message.chat.type != "private":
        chat_id: str = str(message.chat.id)
        clan = await Clans.query.where(
                Clans.chat_id == chat_id
        ).gino.first()
        await clan.update(remain_zero_rock=remain_zero_rock).apply()
        try:
            await message.delete()
        except TelegramBadRequest:
            await message.answer(
                "Предупреждение: Дайте мне права админа, иначе ничего не смогу делать..."
            )
        if remain_zero_rock:
            await message.answer(
                "Ок, я напомню вам за час, о том что будет обнуление камней."
            )
        else:
            await message.answer("Не хотите, как хотите!😝")


@form_router.message(Command('start_remind'))
async def start_remind(message: Message) -> None:
    """Активация напоминания об обнулении камней."""
    await remind(message, remain_zero_rock=True)


@form_router.message(Command('stop_remind'))
async def stop_remind(message: Message) -> None:
    """Деактивация напоминания об обнулении камней."""
    await remind(message, remain_zero_rock=False)
