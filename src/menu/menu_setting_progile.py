from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import and_

from menu.buttons import (
    cancel_button,
    edit_time_button,
    new_button,
    setting_button,
    setting_hero_button,
    subscription_button,
)
from migrations import db
from src import Regisration, SettingProfile, form_router
from src.config import settings
from src.menu.text_menu import go_back, setting_profile
from tables.clans import Clans
from tables.heroes_of_users import HeroesOfUsers


### LEVEL 0
@form_router.message(
    SettingProfile.is_active, F.text == setting_profile["setting_hero"]
)
async def setting_hero(message: Message, state: FSMContext) -> None:
    await setting_hero_button(
        message,
        user_id=(await state.get_data())["user_id"],
        sms="Тут ты можешь добавить или удалить героя, ну и при необходимости переименовать его",
    )
    await state.update_data(level=1)


### LEVEL 1
@form_router.message(
    SettingProfile.is_active, F.text == setting_profile["add_hero"]
)
async def add_hero(message: Message, state: FSMContext) -> None:
    await cancel_button(message, "Какой у тебя ник в игре?")
    await state.update_data(user_id=(await state.get_data())["user_id"])
    await state.set_state(Regisration.name)
    # TODO надо придумать систему возврата


@form_router.message(
    SettingProfile.is_active, F.text == setting_profile["delete_hero"]
)
async def delete_hero(message: Message, state: FSMContext) -> None:
    """Удаляем персонажа, смотрим сколько всего персов и смещаем их к тому который удаляем"""
    if hero := await HeroesOfUsers.query.where(
        HeroesOfUsers.id == (await state.get_data())["hero_id"]
    ).gino.first():
        await new_button(message, f'Герой с ником "{hero.name}" удален!')
        await hero.delete().apply()
        return
    await new_button(
        message, "Я не помню такого героя. Значит и проблем нет :)"
    )


@form_router.message(
    SettingProfile.is_active, F.text == setting_profile["rename_hero"]
)
async def rename_hero(message: Message, state: FSMContext) -> None:
    await message.answer("На какое имя будем менять?")
    await state.set_state(SettingProfile.edit_name)


@form_router.message(SettingProfile.edit_name)
async def edit_name(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    hero = await HeroesOfUsers.query.where(
        and_(
            HeroesOfUsers.id == data["hero_id"],
            HeroesOfUsers.user_id == data["user_id"],
        )
    ).gino.first()
    await hero.update(name=message.text).apply()
    await message.answer(f'Теперь тебя зовут: "{message.text}"!')
    await state.set_state(SettingProfile.is_active)


### LEVEL 0
@form_router.message(
    SettingProfile.is_active, F.text == setting_profile["subscribe"]
)
async def subscribe(message: Message, state: FSMContext) -> None:
    await subscription_button(
        message,
        "Смотри...",
        (await state.get_data())["hero_id"],
    )
    await state.update_data(level=1)


### LEVEL 1
async def engine_subscription(
    message: Message, who_edit: str, text: str, state: FSMContext
) -> None:
    await db.status(db.text(
        f"UPDATE heroes_of_users SET {who_edit}"
        f"WHERE user_id = '{(await state.get_data())['user_id']}'"
        f"    and id = '{(await state.get_data())['hero_id']}';"
    ))
    await subscription_button(
        message,
        text,
        (await state.get_data())["hero_id"],
    )


@form_router.message(
    SettingProfile.is_active, F.text == setting_profile["subscribe_replace_kz"]
)
async def subscribe_replace_kz(message: Message, state: FSMContext) -> None:
    who_edit = "subscription_rock = 'true'"
    text = "Если у вас будет меньше 600 камней, я вам напомню об этом за час до смены КЗ."
    await engine_subscription(message, who_edit, text, state)


@form_router.message(
    SettingProfile.is_active,
    F.text == setting_profile["unsubscribe_replace_kz"],
)
async def unsubscribe_replace_kz(message: Message, state: FSMContext) -> None:
    who_edit = "subscription_rock = 'false'"
    text = "Хорошо, больше не буду вам напоминать про камни... Автоматически."
    await engine_subscription(message, who_edit, text, state)


@form_router.message(
    SettingProfile.is_active, F.text == setting_profile["subscribe_energy"]
)
async def subscribe_energy(message: Message, state: FSMContext) -> None:
    who_edit = "subscription_energy = 'true'"
    text = "Теперь я буду напоминать Вам про энергию."
    await engine_subscription(message, who_edit, text, state)


@form_router.message(
    SettingProfile.is_active, F.text == setting_profile["unsubscribe_energy"]
)
async def unsubscribe_energy(message: Message, state: FSMContext) -> None:
    who_edit = "subscription_energy = 'false'"
    text = "Хорошо, больше не буду Вам напоминать про энергию..."
    await engine_subscription(message, who_edit, text, state)


@form_router.message(
    SettingProfile.is_active,
    F.text == setting_profile["subscribe_description_kz"],
)
async def subscribe_description_kz(
    message: Message, state: FSMContext
) -> None:
    who_edit = "description_of_the_kz = 'true'"
    text = "Теперь я буду присылать Вам краткое описание кланового задания."
    await engine_subscription(message, who_edit, text, state)


@form_router.message(
    SettingProfile.is_active,
    F.text == setting_profile["unsubscribe_description_kz"],
)
async def unsubscribe_description_kz(
    message: Message, state: FSMContext
) -> None:
    who_edit = "description_of_the_kz = 'false'"
    text = "Хорошо, больше не буду присылать Вам краткое описание кланового задания."
    await engine_subscription(message, who_edit, text, state)


### LEVEL 0
@form_router.message(
    SettingProfile.is_active, F.text == setting_profile["update_time"]
)
async def update_time(message: Message, state: FSMContext) -> None:
    await edit_time_button(message, "Меняй...")
    await state.update_data(level=1)


@form_router.message(SettingProfile.time_zone)
async def time_zone(message: Message, state: FSMContext) -> None:
    """Узнаем часовой во сколько происходит смена КЗ"""
    msg = message.text
    if msg in settings.stop_word:
        sms = "Отмена"
        await setting_hero_button(
            message, (await state.get_data())["user_id"], sms
        )
        return
    if msg.isnumeric():
        msg = int(msg)
        if 1 <= msg <= 24:
            hero = await HeroesOfUsers.get(
                int((await state.get_data())["hero_id"])
            )
            if (await state.get_data())["is_tz"]:
                await hero.update(time_change_kz=msg).apply()
            else:
                await hero.update(time_collection_energy=msg).apply()
            sms = "Время умпешно установлено!\n Если Вы ошиблись или время поменяется, всегда можно изменить и тут.\n\n Для этого нажми ⚙️Настройка профиля⚙️ ---> Поменять время..."
            await edit_time_button(message, sms)
        else:
            await message.answer("Введи время по москве!")
    else:
        await message.answer("Вводи цифрами")
    await state.set_state(SettingProfile.is_active)


### LEVEL 1
@form_router.message(
    SettingProfile.is_active,
    F.text == setting_profile["update_time_replace_kz"],
)
async def update_time_replace_kz(message: Message, state: FSMContext) -> None:
    await cancel_button(
        message,
        'Во сколько по москве смена КЗ? Вводи только час.\n Пример: "18"',
    )
    await state.update_data(is_tz=True)
    await state.set_state(SettingProfile.time_zone)


@form_router.message(
    SettingProfile.is_active, F.text == setting_profile["update_time_energy"]
)
async def update_update_time_energytime(
    message: Message, state: FSMContext
) -> None:
    await cancel_button(
        message,
        'Во сколько по москве первый сбор энергии (синька и фиолетка)? Вводи только час.\n Пример: "12"',
    )
    await state.update_data(is_tz=False)
    await state.set_state(SettingProfile.time_zone)


### LEVEL 0
@form_router.message(
    SettingProfile.is_active, F.text == setting_profile["show_data_profile"]
)
async def show_data_profile(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    hero = (
        await HeroesOfUsers.outerjoin(Clans, HeroesOfUsers.clan_id == Clans.id)
        .select()
        .where(
            and_(
                HeroesOfUsers.user_id == data["user_id"],
                HeroesOfUsers.id == data["hero_id"],
            )
        )
        .with_only_columns((HeroesOfUsers, Clans.name_clan))
        .gino.first()
    )
    clan = f'Вы в клане "{hero.name_clan}"' if hero.name_clan else ""
    smena_KZ = str(hero.time_change_kz)  # считываем смену кз
    sbor_energi = str(hero.time_collection_energy)  # считываем сбор энергии

    if hero.subscription_rock:
        subscription_Rock_text = "✅ Вы подписаны на оповещение по камням."
    else:
        subscription_Rock_text = "❗️ Вы не подписаны на оповещение по камням."
    if hero.subscription_energy:
        subscription_Energi_text = (
            "✅ Вы подписаны на оповещение по сбору энергии."
        )
    else:
        subscription_Energi_text = (
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
        f"{subscription_Rock_text}\n"
        f"{subscription_Energi_text}\n"
        f"{description_of_the_kz_text}\n"
        f"Время смены КЗ: {smena_KZ}:30 по мск \n"
        f"Время сбора первой энергии: {sbor_energi}:00 по мск\n"
        f"{clan}",
    )


@form_router.message(SettingProfile.is_active, F.text == go_back)
async def go_back_setting_profile(message: Message, state: FSMContext) -> None:
    if (await state.get_data())["level"] == 1:
        await setting_button(message, "Ок, вернулись.")
        await state.update_data(level=0)
    else:
        await new_button(
            message,
            "Погнали, назад, в главное меню.",
        )
        await state.clear()
