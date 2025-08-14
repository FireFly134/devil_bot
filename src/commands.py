"""Файл с командами."""
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from chat_commands import chat_start
from menu.buttons import new_button
from services.statistics import statistics
from src import Regisration, form_router
from tables.heroes_of_users import HeroesOfUsers
from tables.telegram_users import User


async def ensure_user_exists(message: Message, state: FSMContext) -> User:
    """Обеспечивает существование пользователя в базе данных."""
    existing_user = await User.query.where(
        User.user_id == message.from_user.id
    ).gino.first()

    if existing_user:
        return existing_user

    # Создаем нового пользователя
    user = await User(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
        language_code=message.from_user.language_code,
    ).create()

    return user


async def regisration(message: Message, state: FSMContext) -> None:
    """Регистрация пользователя."""
    try:
        user = await ensure_user_exists(message, state)

        await message.answer(
            "Я тебя не помню. Давай знакомиться! Какой у тебя ник в игре?"
        )
        await state.update_data(user_id=user.id)
        await state.set_state(Regisration.name)
    except Exception as e:
        # Логируем ошибку и отправляем сообщение пользователю
        print(
            f"Ошибка при регистрации пользователя {message.from_user.id}: {e}"
        )
        await message.answer(
            "Произошла ошибка при регистрации. Попробуйте еще раз."
        )


@form_router.message(CommandStart())
@statistics(text="/start", is_state=True)
async def start(message: Message, state: FSMContext) -> None:
    """Команда для начала работы с ботом."""
    if message.chat.type == "private":
        hero_user_search = (
            await HeroesOfUsers.join(User)
            .select()
            .where(User.user_id == message.from_user.id)
            .with_only_columns(HeroesOfUsers)
            .gino.first()
        )
        if hero_user_search:
            sms = f"Привет, {hero_user_search.name}"
            await new_button(message, sms)
            return
        await regisration(message, state)
    else:
        await chat_start(message)


@form_router.message(Command("help"))
@statistics(text="/help", is_state=True)
async def helper(message: Message, state: FSMContext) -> None:
    """Команда для вывода вспомогательной инструкции."""
    if message.chat.type == "private":
        user_id: int = message.from_user.id
        user_exists = await User.query.where(
            User.user_id == user_id
        ).gino.first()
        if user_exists:
            await new_button(
                message,
                'Напиши "Привет" чтобы проверить свой ник.\n Можешь кидать количество камней (цифрами) и спросить сколько у тебя камней.\nЗагляни в настройки пользователя, там можешь подписаться на напоминания по сбору халявной энергии или на напоминания по камням за час до смены К.З.(или отписаться)\nЕсли у тебя не один профель в игре, можешь добавить его ник и также кидать на него кол-во камней, но можно добавить не больше 5 героев!\nЕсли возникли проблемы с кнопками напиши /start (не помогло напиши мне @Menace134)',
            )
            # info = pd.read_sql(  # noqa: E800
            #     f"SELECT COUNT(*) FROM admins WHERE user_id = '{user_id}';",  # noqa: E800
            #     engine, # noqa: E800
            # ) # noqa: E800
            # if info.loc[0, "count"] != 0: # noqa: E800
            #     context.bot.send_message( # noqa: E800
            #         chat_id=user_id, # noqa: E800
            #         text=f'Для тебя, {update.message.from_user.first_name}, ещё есть настройки администратора.\n Там ты сможешь:\n - отправить напоминалку игроку\n- редактировать сообщение напоминалки\n- отправить ВСЕМ сообщение\n- написать в "флудилку" от имени бота.\n- убрать игрока из клана☠', # noqa: E800
            #     ) # noqa: E800
        else:
            await regisration(message, state)
    else:
        await message.answer("Привет, скоро будет инструкция...!")
