from datetime import datetime, timedelta

from pytz import timezone

from migrations import db
from services.send_message import send_msg_mv2
from tables.events import Events
from tables.telegram_users import User

tz = timezone("Europe/Moscow")


async def reminder_events():
    time = datetime.now(tz=tz)  # текущее время
    time_add_two_days = (time + timedelta(days=2)).date()
    time_add_two_week = (
        time + timedelta(days=16)
    ).date()  # через 2 дня будет ивент и через 2 недели будет повтор поэтому 14+2=16
    ### Проверка на наличия энергии по времени для подписчиков ###
    info_event = await Events.query.where(
        Events.event_date == time_add_two_days
    ).gino.all()
    info_user = await User.query.where(User.subscription_event).gino.all()
    if info_event:
        await db.status(
            db.text(
                "UPDATE events SET event_date = :new_date WHERE event_date = :old_date;"
            ),
            {"old_date": time_add_two_days, "new_date": time_add_two_week},
        )
        for event in info_event:
            text = (
                str(event.description)
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
            for user in info_user:
                await send_msg_mv2(
                    user_id=user.user_id, sms=f"*Через два дня {text}*"
                )
