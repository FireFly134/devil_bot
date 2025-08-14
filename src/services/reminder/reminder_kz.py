"""Напоминалка по подпискам"""
from datetime import datetime, timedelta

from pytz import timezone
from sqlalchemy import and_

from services.send_message import send_msg, send_msg_mv2
from tables.clans import Clans
from tables.heroes_of_users import HeroesOfUsers
from tables.telegram_users import User
from tables.text_table import TextTable

tz = timezone("Europe/Moscow")


async def reminder_private_change_kz(time_kz: datetime) -> None:
    """Напоминание в личку про смену КЗ."""
    heroes = (
        await HeroesOfUsers.join(User)
        .select()
        .where(
            and_(
                HeroesOfUsers.time_change_kz == int(time_kz.strftime("%H")),
                HeroesOfUsers.subscription_rock,
            )
        )
        .with_only_columns(
            (HeroesOfUsers.id, HeroesOfUsers.name, User.user_id)
        )
        .gino.all()
    )

    if heroes:
        for hero in heroes:
            await send_msg(
                user_id=hero.user_id,
                sms=f"До смены кланового задания остался 1 час! ({hero.name})",
            )


async def description_new_kz(time: datetime) -> None:
    """Описание нового КЗ в личку."""
    heroes = (
        await HeroesOfUsers.join(User)
        .select()
        .where(
            and_(
                HeroesOfUsers.time_change_kz == int(time.strftime("%H")),
                HeroesOfUsers.description_of_the_kz,
            )
        )
        .with_only_columns(
            (HeroesOfUsers.id, HeroesOfUsers.name, User.user_id)
        )
        .gino.all()
    )

    if heroes:
        text_info = await TextTable.query.where(
            TextTable.name_text == time.strftime("%w")
        ).gino.first()
        for hero in heroes:
            name = (
                str(hero.name)
                .replace("_", "\\_")
                .replace("*", "\\*")
                .replace("[", "\\[")
                .replace("]", "\\]")
                .replace("(", "\\(")
                .replace(")", "\\)")
                .replace("`", "\\`")
                .replace("~", "\\~")
                .replace(">", "\\>")
                .replace("#", "\\#")
                .replace("+", "\\+")
                .replace("=", "\\=")
                .replace("-", "\\-")
                .replace("|", "\\|")
                .replace("{", "\\{")
                .replace("}", "\\}")
                .replace(".", "\\.")
                .replace("!", "\\!")
            )
            await send_msg_mv2(
                user_id=hero.user_id, sms=f"{name}\!\n{text_info.text}"
            )


async def reminder_change_kz_in_chat_clans(time_kz: datetime) -> None:
    """Напоминание в чат клана про смену КЗ."""
    clans = await Clans.query.where(
        and_(
            Clans.start,
            Clans.subscription_rock,
            Clans.time_kz == int(time_kz.strftime("%H")),
        )
    ).gino.all()

    if clans:
        for clan in clans:
            await send_msg(
                user_id=clan.chat_id,
                sms="До смены кланового задания остался 1 час!",
                message_thread_id=clan.thread_id,
            )


async def description_new_kz_in_chat_clans(time: datetime) -> None:
    """Описание нового КЗ в чат."""
    clans = await Clans.query.where(
        and_(
            Clans.start,
            Clans.description_of_the_kz,
            Clans.time_kz == int(time.strftime("%H")),
        )
    ).gino.all()
    if clans:
        text_info = await TextTable.query.where(
            TextTable.name_text == time.strftime("%w")
        ).gino.first()
        for clan in clans:
            await send_msg_mv2(
                user_id=clan.chat_id,
                sms=text_info.text,
                message_thread_id=clan.thread_id,
            )


async def reminder_kz():
    time = datetime.now(tz=tz)
    time_kz = time + timedelta(hours=1)
    await reminder_private_change_kz(time_kz)
    await description_new_kz(time)
    await reminder_change_kz_in_chat_clans(time_kz)
    await description_new_kz_in_chat_clans(time)
