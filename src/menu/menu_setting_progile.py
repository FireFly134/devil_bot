"""Меню настройки героя."""
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from menu.buttons import (
    cancel_button,
    edit_time_button,
    new_button,
    setting_hero_button,
    subscription_button,
)
from migrations import db
from services.statistics import statistics
from src import Regisration, SettingProfile, form_router
from src.config import settings
from src.menu.text_menu import cancel, setting_profile
from tables.clans import Clans
from tables.heroes_of_users import HeroesOfUsers


# LEVEL 0
@form_router.message(
    SettingProfile.is_active, F.text == setting_profile["setting_hero"]
)
async def setting_hero(message: Message, state: FSMContext) -> None:
    """Переход в настройки героя."""
    state_data = await state.get_data()

    # Безопасно получаем hero_user_id, если его нет - используем user_id из сообщения
    hero_user_id = state_data.get("hero_user_id", message.from_user.id)

    await setting_hero_button(
        message,
        user_id=hero_user_id,
        sms="Тут ты можешь добавить или удалить героя, ну и при необходимости переименовать его",
        name=state_data.get("name", "Неизвестно"),
    )
    await state.update_data(level=1)


# LEVEL 1
@form_router.message(
    SettingProfile.is_active, F.text == setting_profile["add_hero"]
)
@statistics(text=setting_profile["add_hero"], is_state=True)
async def add_hero(message: Message, state: FSMContext) -> None:
    """Добавляем героя."""
    await cancel_button(message, "Какой у тебя ник в игре?")
    state_data = await state.get_data()
    user_id = state_data.get("hero_user_id", message.from_user.id)
    await state.update_data(user_id=user_id)
    await state.set_state(Regisration.name)
    # TODO надо придумать систему возврата


@form_router.message(
    SettingProfile.is_active, F.text.startswith(setting_profile["delete_hero"])
)
@statistics(text=setting_profile["delete_hero"], is_state=True)
async def delete_hero(message: Message, state: FSMContext) -> None:
    """Удаляем персонажа, смотрим сколько всего персов и смещаем их к тому который удаляем."""
    hero = await HeroesOfUsers.query.where(
        HeroesOfUsers.id == (await state.get_data())["hero_id"]
    ).gino.first()
    if hero:
        await new_button(message, f'Герой с ником "{hero.name}" удален!')
        await hero.delete()
        return
    await new_button(
        message, "Я не помню такого героя. Значит и проблем нет :)"
    )


@form_router.message(
    SettingProfile.is_active, F.text.startswith(setting_profile["rename_hero"])
)
@statistics(text=setting_profile["rename_hero"], is_state=True)
async def rename_hero(message: Message, state: FSMContext) -> None:
    """Начинаем редактирование имени героя."""
    await cancel_button(message, "На какое имя будем менять?")
    await state.set_state(SettingProfile.edit_name)


@form_router.message(SettingProfile.edit_name)
async def edit_name(message: Message, state: FSMContext) -> None:
    """Редактируем имя героя."""
    if message.text in settings.stop_word or message.text in cancel:
        await state.set_state(SettingProfile.is_active)
        await setting_hero(message, state)
        return
    state_data = await state.get_data()
    hero = await HeroesOfUsers.query.where(
        HeroesOfUsers.id == state_data["hero_id"]
    ).gino.first()
    await hero.update(name=message.text).apply()
    await message.answer(f'Теперь тебя зовут: "{message.text}"!')
    await state.update_data(name=message.text)
    await state.set_state(SettingProfile.is_active)
    await setting_hero(message, state)


# LEVEL 0
@form_router.message(
    SettingProfile.is_active, F.text == setting_profile["subscribe"]
)
async def subscribe(message: Message, state: FSMContext) -> None:
    """Переходим в настройки подписок."""
    await subscription_button(
        message,
        "Смотри...",
        (await state.get_data())["hero_id"],
    )
    await state.update_data(level=1)


# LEVEL 1
async def engine_subscription(
    message: Message, who_edit: str, text: str, state: FSMContext
) -> None:
    """Подписка на оповещение по получению энергии."""
    await db.status(
        db.text(
            "UPDATE heroes_of_users SET {who_edit}, updated_at = now() WHERE id = {hero_id};".format(
                who_edit=who_edit,
                hero_id=(await state.get_data())["hero_id"],
            )
        )
    )

    await subscription_button(
        message,
        text,
        (await state.get_data())["hero_id"],
    )


async def engine_subscription_event(
    message: Message, who_edit: str, text: str, state: FSMContext
) -> None:
    """Подписка на оповещение по получению энергии."""
    await db.status(
        db.text(
            "UPDATE users SET {who_edit}, updated_at = now() WHERE user_id = {user_id};".format(
                who_edit=who_edit,
                user_id=message.from_user.id,
            )
        )
    )

    await subscription_button(
        message,
        text,
        (await state.get_data())["hero_id"],
    )


@form_router.message(
    SettingProfile.is_active, F.text == setting_profile["subscribe_replace_kz"]
)
@statistics(text=setting_profile["subscribe_replace_kz"], is_state=True)
async def subscribe_replace_kz(message: Message, state: FSMContext) -> None:
    """Подписка на оповещение об обнулении камней."""
    who_edit = "subscription_rock = 'true'"
    text = f"Если у вас будет меньше {settings.MAX_COUNT_ROCKS} камней, я вам напомню об этом за час до смены КЗ."
    await engine_subscription(message, who_edit, text, state)


@form_router.message(
    SettingProfile.is_active,
    F.text == setting_profile["unsubscribe_replace_kz"],
)
@statistics(text=setting_profile["unsubscribe_replace_kz"], is_state=True)
async def unsubscribe_replace_kz(message: Message, state: FSMContext) -> None:
    """Отписка от оповещения об обнулении камней."""
    who_edit = "subscription_rock = 'false'"
    text = "Хорошо, больше не буду вам напоминать про камни... Автоматически."
    await engine_subscription(message, who_edit, text, state)


@form_router.message(
    SettingProfile.is_active, F.text == setting_profile["subscribe_energy"]
)
@statistics(text=setting_profile["subscribe_energy"], is_state=True)
async def subscribe_energy(message: Message, state: FSMContext) -> None:
    """Подписка на оповещение по получению энергии."""
    who_edit = "subscription_energy = 'true'"
    text = "Теперь я буду напоминать Вам про энергию."
    await engine_subscription(message, who_edit, text, state)


@form_router.message(
    SettingProfile.is_active, F.text == setting_profile["unsubscribe_energy"]
)
@statistics(text=setting_profile["unsubscribe_energy"], is_state=True)
async def unsubscribe_energy(message: Message, state: FSMContext) -> None:
    """Отписка от оповещения по получению энергии."""
    who_edit = "subscription_energy = 'false'"
    text = "Хорошо, больше не буду Вам напоминать про энергию..."
    await engine_subscription(message, who_edit, text, state)


@form_router.message(
    SettingProfile.is_active,
    F.text == setting_profile["subscribe_description_kz"],
)
@statistics(text=setting_profile["subscribe_description_kz"], is_state=True)
async def subscribe_description_kz(
    message: Message, state: FSMContext
) -> None:
    """Подписка на описание кланового задания."""
    who_edit = "description_of_the_kz = 'true'"
    text = "Теперь я буду присылать Вам краткое описание кланового задания."
    await engine_subscription(message, who_edit, text, state)


@form_router.message(
    SettingProfile.is_active,
    F.text == setting_profile["unsubscribe_description_kz"],
)
@statistics(text=setting_profile["unsubscribe_description_kz"], is_state=True)
async def unsubscribe_description_kz(
    message: Message, state: FSMContext
) -> None:
    """Отписка от описания кланового задания."""
    who_edit = "description_of_the_kz = 'false'"
    text = "Хорошо, больше не буду присылать Вам краткое описание кланового задания."
    await engine_subscription(message, who_edit, text, state)


@form_router.message(
    SettingProfile.is_active, F.text == setting_profile["subscribe_event"]
)
@statistics(text=setting_profile["subscribe_event"], is_state=True)
async def subscribe_energy(message: Message, state: FSMContext) -> None:
    """Подписка на оповещение по получению энергии."""
    who_edit = "subscription_event = 'true'"
    text = "Теперь я буду оповещать Вас о событиях."
    await engine_subscription_event(message, who_edit, text, state)


@form_router.message(
    SettingProfile.is_active, F.text == setting_profile["unsubscribe_event"]
)
@statistics(text=setting_profile["unsubscribe_event"], is_state=True)
async def unsubscribe_energy(message: Message, state: FSMContext) -> None:
    """Отписка от оповещения по получению энергии."""
    who_edit = "subscription_event = 'false'"
    text = "Хорошо, больше не буду оповещать Вас о событиях..."
    await engine_subscription_event(message, who_edit, text, state)


# LEVEL 0
@form_router.message(
    SettingProfile.is_active, F.text == setting_profile["update_time"]
)
@statistics(text=setting_profile["update_time"], is_state=True)
async def update_time(message: Message, state: FSMContext) -> None:
    """Переход в настройки обновления времени."""
    await edit_time_button(
        message, int((await state.get_data())["hero_id"]), "Меняй..."
    )
    await state.update_data(level=1)


@form_router.message(SettingProfile.time_zone)
async def time_zone(message: Message, state: FSMContext) -> None:
    """Узнаем часовой во сколько происходит смена КЗ."""
    msg = message.text
    state_data = await state.get_data()
    if msg in settings.stop_word or msg in cancel:
        sms = "Ок... Галя, у нас отмена!"
        await state.set_state(SettingProfile.is_active)
        await edit_time_button(message, int(state_data["hero_id"]), sms)
        return
    if msg.isnumeric():
        msg = int(msg)
        if 1 <= msg <= 24:
            hero = await HeroesOfUsers.get(int(state_data["hero_id"]))
            if (await state.get_data())["is_tz"]:
                await hero.update(time_change_kz=msg).apply()
            else:
                await hero.update(time_collection_energy=msg).apply()
            sms = "Время успешно установлено!\n Если Вы ошиблись или время поменяется, всегда можно изменить и тут.\n\n Для этого нажми ⚙️Настройка профиля⚙️ ---> Поменять время..."
            await edit_time_button(message, int(state_data["hero_id"]), sms)
            await state.set_state(SettingProfile.is_active)
        else:
            await message.answer(
                "Какое странное время 😑 ... давай в пределах 24 часов. Введи ещё раз."
            )
    else:
        await message.answer("Вводи цифрами")


# LEVEL 1
@form_router.message(
    SettingProfile.is_active,
    F.text.startswith(setting_profile["update_time_replace_kz"]),
)
@statistics(text=setting_profile["update_time_replace_kz"], is_state=True)
async def update_time_replace_kz(message: Message, state: FSMContext) -> None:
    """Узнаем часовой во сколько происходит смена КЗ."""
    await cancel_button(
        message,
        'Во сколько по москве смена КЗ? Вводи только час.\nПример: "18"',
    )
    await state.update_data(is_tz=True)
    await state.set_state(SettingProfile.time_zone)


@form_router.message(
    SettingProfile.is_active,
    F.text.startswith(setting_profile["update_time_energy"]),
)
@statistics(text=setting_profile["update_time_energy"], is_state=True)
async def update_update_time_energytime(
    message: Message, state: FSMContext
) -> None:
    """Узнаем часовой во сколько происходит смена КЗ."""
    await cancel_button(
        message,
        'Во сколько по москве первый сбор энергии (синька и фиолетка)? Вводи только час.\n Пример: "12"',
    )
    await state.update_data(is_tz=False)
    await state.set_state(SettingProfile.time_zone)


# LEVEL 0
@form_router.message(
    SettingProfile.is_active, F.text == setting_profile["show_data_profile"]
)
@statistics(text=setting_profile["show_data_profile"], is_state=True)
async def show_data_profile(message: Message, state: FSMContext) -> None:
    """Показывает данные профиля."""
    state_data = await state.get_data()
    hero = (
        await HeroesOfUsers.outerjoin(Clans)
        .select()
        .where(HeroesOfUsers.id == state_data["hero_id"])
        .with_only_columns((HeroesOfUsers, Clans.name_clan))
        .gino.first()
    )
    clan = f'Вы в клане "{hero.name_clan}"' if hero.name_clan else ""
    smena_kz = str(hero.time_change_kz)  # считываем смену кз
    sbor_energi = str(hero.time_collection_energy)  # считываем сбор энергии

    if hero.subscription_rock:
        subscription_rock_text = "✅ Вы подписаны на оповещение по камням."
    else:
        subscription_rock_text = "❗️ Вы не подписаны на оповещение по камням."
    if hero.subscription_energy:
        subscription_energi_text = (
            "✅ Вы подписаны на оповещение по сбору энергии."
        )
    else:
        subscription_energi_text = (
            "❗️ Вы не подписаны на оповещение по сбору энергии."
        )
    if hero.description_of_the_kz:
        description_of_the_kz_text = (
            "✅ Вы подписаны на ежедневное описание КЗ."
        )
    else:
        description_of_the_kz_text = (
            "❗️ Вы не подписаны на ежедневное описание КЗ."
        )
    await message.answer(
        f"Ваш ник в игре: {hero.name}\n"
        f"{subscription_rock_text}\n"
        f"{subscription_energi_text}\n"
        f"{description_of_the_kz_text}\n"
        f"Время смены КЗ: {smena_kz}:30 по мск \n"
        f"Время сбора первой энергии: {sbor_energi}:00 по мск\n"
        f"{clan}",
    )
