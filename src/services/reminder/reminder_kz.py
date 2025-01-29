"""Напоминалка по подпискам"""
import logging
from datetime import datetime, timedelta

from sqlalchemy import and_

from services.send_message import send_msg, send_msg_mv2
from tables.clans import Clans
from tables.heroes_of_users import HeroesOfUsers
from tables.telegram_users import User
from tables.text_table import TextTable


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
        logging.info(f"reminder_private_change_kz GO = {len(heroes)}")
        for hero in heroes:
            await send_msg(
                user_id=hero.user_id,
                text=f"До смены кланового задания остался 1 час! ({hero.name})",
            )
            logging.info(f"reminder_private_change_kz hero.id = {hero.id}")


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
        logging.info(f"description_new_kz GO = {len(heroes)}")
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
                user_id=hero.user_id, text=f"{name}\!\n{text_info.text}"
            )
            logging.info(f"description_new_kz hero.id = {hero.id}")


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
        logging.info(f"reminder_change_kz_in_chat_clans GO = {len(clans)}")
        for clan in clans:
            await send_msg(
                user_id=clan.chat_id,
                text="До смены кланового задания остался 1 час!",
            )
            logging.info(
                f"reminder_change_kz_in_chat_clans clan.id = {clan.id}"
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
        logging.info(f"description_new_kz_in_chat_clans GO = {len(clans)}")
        text_info = await TextTable.query.where(
            TextTable.name_text == time.strftime("%w")
        ).gino.first()
        for clan in clans:
            await send_msg_mv2(user_id=clan.chat_id, text=text_info.text)
            logging.info(
                f"description_new_kz_in_chat_clans clan.id = {clan.id}"
            )


async def reminder_kz():
    time = datetime.now()
    time_kz = time + timedelta(hours=1)
    await reminder_private_change_kz(time_kz)
    await description_new_kz(time)
    await reminder_change_kz_in_chat_clans(time_kz)
    await description_new_kz_in_chat_clans(time)
