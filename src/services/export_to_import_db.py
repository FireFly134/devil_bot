"""Скрипт для переноса данных их старой бд в новую."""

import asyncio

from sqlalchemy import create_engine, text

from migrations import run_connection_db
from tables.heroes_of_users import HeroesOfUsers
from tables.telegram_users import User


async def export_to_import_user(engine) -> None:
    users = engine.execute(text("SELECT * FROM telegram_users_id;"))
    for user in users:
        """user_id,first_name,last_name,username,language_code,send_msg"""
        if not (
            await User.query.where(User.user_id == user.user_id).gino.first()
        ):
            new_user = await User(
                user_id=user.user_id,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                language_code=user.language_code,
                send_msg=user.send_msg,
            ).create()
            await export_to_import_heroes(user.user_id, new_user.id, engine)


async def export_to_import_heroes(
    tlegram_id: int, user_id: int, engine
) -> None:
    heros = engine.execute(
        text(f"SELECT * FROM heroes_of_users WHERE user_id = {tlegram_id};")
    )
    for hero in heros:
        """id,user_id,name,rock,clan_id,time_change_kz,time_collection_energy,subscription_rock,subscription_energy,description_of_the_kz"""
        await HeroesOfUsers(
            user_id=user_id,
            name=hero.name,
            rock=hero.rock,
            time_change_kz=int(hero.time_change_kz),
            time_collection_energy=int(hero.time_collection_energy),
            subscription_rock=hero.subscription_rock,
            subscription_energy=hero.subscription_energy,
            description_of_the_kz=hero.description_of_the_kz,
        ).create()


async def main() -> None:
    """
    Переносу подлежит 2 таблицы:
     - users в старой БД это telegram_users_id
     - heroes_of_users
    """
    engine = create_engine("postgresql://login:password@host:port/name_db")
    await run_connection_db()
    await export_to_import_user(engine)


if __name__ == "__main__":
    asyncio.run(main())
