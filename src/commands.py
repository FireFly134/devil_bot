from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from buttons import new_button
from chat_commands import chat_start
from src import Regisration, form_router
from tables.heroes_of_users import HeroesOfUsers
from tables.telegram_users import User


async def regisration(
    message: Message, user_id: int, state: FSMContext
) -> None:
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
                await regisration(message, user_id, state)
    else:
        await chat_start(message)


@form_router.message(Command("help"))
async def helper(message: Message, state: FSMContext) -> None:
    if message.chat.type == "private":
        if message.from_user is not None:
            user_id: int = int(message.from_user.id)
            if await User.query.where(User.user_id == user_id).gino.first():
                await new_button(
                    message,
                    'Напиши "Привет" чтобы проверить свой ник.\n Можешь кидать количество камней (цифрами) и спросить сколько у тебя камней.\nЗагляни в настройки пользователя, там можешь подписаться на напоминания по сбору халявной энергии или на напоминания по камням за час до смены К.З.(или отписаться)\nЕсли у тебя не один профель в игре, можешь добавить его ник и также кидать на него кол-во камней, но можно добавить не больше 5 героев!\nЕсли возникли проблемы с кнопками напиши /start (не помогло напиши мне @Menace134)',
                )
                # info = pd.read_sql(
                #     f"SELECT COUNT(*) FROM admins WHERE user_id = '{user_id}';",
                #     engine,
                # )
                # if info.loc[0, "count"] != 0:
                #     context.bot.send_message(
                #         chat_id=user_id,
                #         text=f'Для тебя, {update.message.from_user.first_name}, ещё есть настройки администратора.\n Там ты сможешь:\n - отправить напоминалку игроку\n- редактировать сообщение напоминалки\n- отправить ВСЕМ сообщение\n- написать в "флудилку" от имени бота.\n- убрать игрока из клана☠',
                #     )
            else:
                await regisration(message, user_id, state)
    else:
        await message.answer("Привет, скоро будет инструкция...!")
