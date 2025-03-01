"""Файл с командами для чата/клана."""
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src import UpdateTimeChangeClanTask, form_router
from tables.clans import Clans


async def chat_start(message: Message) -> None:
    """Запуск активности в чате."""
    chat_id = str(message.chat.id)
    clan = await Clans.query.where(Clans.chat_id == chat_id).gino.first()
    if clan:
        if clan.start:
            await message.answer(
                f"Привет, {clan.name_clan}!",
            )
        else:
            await clan.update(start=True).apply()
            await message.answer(
                f"Привет, {clan.name_clan}!\nЯ снова с вами!😈",
            )
    else:
        await Clans(
            chat_id=chat_id,
            name_clan=message.chat.title,
        ).create()
        await message.answer("Привет, меня зовут Люцик!")


@form_router.message(Command("stop"))
async def stop(message: Message) -> None:
    """Остановка активности в чате."""
    if message.chat.type != "private":
        chat_id: str = str(message.chat.id)
        clan = await Clans.query.where(Clans.chat_id == chat_id).gino.first()
        if clan and clan.start:
            await clan.update(start=False).apply()
            await message.answer("Ок, я все понял!☹️\nЯ пошел...")
            return
        await message.answer("А что я? Я молчу!☹️")


@form_router.callback_query(UpdateTimeChangeClanTask.hour)
async def add_hour_for_change_clan_task(
    message: Message, state: FSMContext
) -> None:
    """Изменения времени смены КЗ в чате."""
    if (await state.get_data())["user_id"] != message.from_user.id:
        return
    chat_id: str = str(message.chat.id)
    msg: str = message.text
    if msg.isnumeric():
        if 1 <= int(msg) <= 24:
            clan = await Clans.query.where(
                Clans.chat_id == chat_id
            ).gino.first()
            if clan:
                await clan.update(time_kz=msg).apply()
            else:
                await Clans(
                    chat_id=chat_id,
                    name_clan=message.chat.title,
                    time_kz=msg,
                    start=False,
                ).create()
            await message.answer("Время умпешно установлено!")
            await state.clear()
        else:
            await message.answer("Введи время по москве!")
    else:
        await message.answer("Вводи цифрами")


@form_router.message(Command("update_time_change_clan_task"))
async def update_time_change_clan_task(
    message: Message, state: FSMContext
) -> None:
    """Команда для изменения времени смены КЗ в чате."""
    if message.chat.type != "private":
        await state.update_data(user_id=message.from_user.id)
        await state.set_state(UpdateTimeChangeClanTask.hour)
        await delete_message(message)
        await message.answer(
            'Во сколько по москве смена КЗ? Вводи только час.\n Пример: "18"'
        )


async def remind(message: Message, remain_zero_rock: bool) -> None:
    """Активация/деактивация напоминания об обнуление камней."""
    clan = await Clans.query.where(
        Clans.chat_id == str(message.chat.id)
    ).gino.first()
    if clan and message.chat.type != "private":
        await clan.update(remain_zero_rock=remain_zero_rock).apply()
        await delete_message(message)
        if remain_zero_rock:
            await message.answer(
                "Ок, я напомню вам за час, о том что будет обнуление камней."
            )
        else:
            await message.answer("Не хотите, как хотите!😝")


@form_router.message(Command("start_remind"))
async def start_remind(message: Message) -> None:
    """Активация напоминания об обнулении камней."""
    await remind(message, remain_zero_rock=True)


@form_router.message(Command("stop_remind"))
async def stop_remind(message: Message) -> None:
    """Деактивация напоминания об обнулении камней."""
    await remind(message, remain_zero_rock=False)


async def delete_message(message: Message) -> None:
    """Удаление сообщения в чате."""
    try:
        await message.delete()
    except TelegramBadRequest:
        await message.answer(
            "Предупреждение: Дайте мне права админа, иначе ничего не смогу делать..."
        )
