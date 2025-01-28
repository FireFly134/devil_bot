"""Напоминание в чат про обнуления камушков за 1 час. И обнуление."""
from sqlalchemy import and_
import logging
from migrations import db
from services.send_message import send_msg

from tables.heroes_of_users import HeroesOfUsers
from tables.clans import Clans

async def reminder_zero(text="До обнуления камушков остался 1 час!") -> None:
    """Напоминание в чате."""
    info_clans = await Clans.query.where(
        and_(
            Clans.start,
            Clans.remain_zero_rock,
        )
    ).gino.all()
    for clan in info_clans:
        await send_msg(user_id=clan.chat_id, sms=text)

async def clear_rock() -> None:
    """Обнуление камней у всех пользователей."""
    info_heroes_of_users = await HeroesOfUsers.query.where(HeroesOfUsers.rock > 0).gino.all()
    if info_heroes_of_users:
        str_list_to_zero = ','.join([str(id_hero.id) for id_hero in info_heroes_of_users])
        logging.info(f"clear_rock GO = {len(info_heroes_of_users)}")
        await db.status(
            "UPDATE heroes_of_users SET rock = '0' "
            f"WHERE id in ({str_list_to_zero});"
        )
    await reminder_zero(text="Камушки обнулились. Пора набивать новые!😎")