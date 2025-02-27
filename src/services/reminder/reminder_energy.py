"""Напоминалка по подпискам о сборе энергии."""
from datetime import datetime, timedelta

from pytz import timezone
from sqlalchemy import and_, or_

from services.send_message import send_msg_mv2
from tables.heroes_of_users import HeroesOfUsers
from tables.telegram_users import User

tz = timezone("Europe/Moscow")


async def reminder_energy():
    time = datetime.now(tz=tz)
    time2_energy = time - timedelta(hours=6)
    time3_energy = time - timedelta(hours=9)
    heroes = (
        await HeroesOfUsers.join(User)
        .select()
        .where(
            and_(
                or_(
                    HeroesOfUsers.time_collection_energy
                    == int(time.strftime("%H")),
                    HeroesOfUsers.time_collection_energy
                    == int(time2_energy.strftime("%H")),
                    HeroesOfUsers.time_collection_energy
                    == int(time3_energy.strftime("%H")),
                ),
                HeroesOfUsers.subscription_energy,
            )
        )
        .with_only_columns(
            (HeroesOfUsers.id, HeroesOfUsers.name, User.user_id)
        )
        .gino.all()
    )
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
            user_id=hero.user_id,
            sms=f"*Зайди в игру и забери халявную энергию*\. \({name}\)",
        )
