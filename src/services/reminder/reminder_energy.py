"""Напоминалка по подпискам о сборе энергии."""
from datetime import datetime, timedelta

from sqlalchemy import and_, or_

from services.send_message import send_msg_mv2
from tables.heroes_of_users import HeroesOfUsers


async def reminder_energy():
    time = datetime.now()
    time2_energy = time - timedelta(hours=6)
    time3_energy = time - timedelta(hours=9)
    heroes = await HeroesOfUsers.query.where(
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
    ).gino.all()
    for hero in heroes:
        name = (
            str(hero.name)
            .replace("_", "\_")
            .replace("*", "\*")
            .replace("[", "\[")
            .replace("]", "\]")
            .replace("(", "\(")
            .replace(")", "\)")
            .replace("`", "\`")
            .replace("~", "\~")
            .replace(">", "\>")
            .replace("#", "\#")
            .replace("+", "\+")
            .replace("=", "\=")
            .replace("-", "\-")
            .replace("|", "\|")
            .replace("{", "\{")
            .replace("}", "\}")
            .replace(".", "\.")
            .replace("!", "\!")
        )
        await send_msg_mv2(
            user_id=hero.user_id,
            text=f"*Зайди в игру и забери халявную энергию*\. \({name}\)",
        )
