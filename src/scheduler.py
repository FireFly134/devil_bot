"""Файл для запуска планировщика."""
import logging
from asyncio import Future, run

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

from src.request import main as get_news
from src.services.reminder.reminder_and_cleaner_rock import (
    clear_rock,
    reminder_zero,
)
from src.services.reminder.reminder_energy import reminder_energy
from src.services.reminder.reminder_events import reminder_events
from src.services.reminder.reminder_kz import reminder_kz


async def scheduler() -> None:
    """Запуск планировщика."""
    logging.info("Scheduler starting...")
    io_scheduler = AsyncIOScheduler()
    io_scheduler.add_job(
        get_news,
        "cron",
        id="get_news",
        hour="*",
        minute="*/5",
        timezone=timezone("Europe/Moscow"),
        replace_existing=True,
    )
    io_scheduler.add_job(
        reminder_zero,
        "cron",
        id="reminder_zero",
        hour="14",
        minute="0",
        timezone=timezone("Europe/Moscow"),
        replace_existing=True,
    )
    io_scheduler.add_job(
        clear_rock,
        "cron",
        id="clear_rock",
        hour="15",
        minute="0",
        timezone=timezone("Europe/Moscow"),
        replace_existing=True,
    )
    io_scheduler.add_job(
        reminder_energy,
        "cron",
        id="reminder_energy",
        hour="*",
        minute="0",
        timezone=timezone("Europe/Moscow"),
        replace_existing=True,
    )
    io_scheduler.add_job(
        reminder_kz,
        "cron",
        id="reminder_kz",
        hour="*",
        minute="30",
        timezone=timezone("Europe/Moscow"),
        replace_existing=True,
    )
    io_scheduler.add_job(
        reminder_events,
        "cron",
        id="reminder_events",
        hour="12",
        minute="0",
        timezone=timezone("Europe/Moscow"),
        replace_existing=True,
    )
    logging.info("added tasks to cron scheduler")
    io_scheduler.start()
    try:
        await Future()  # Держим планировщик запущенным
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler stopping...")
    finally:
        io_scheduler.shutdown()
        logging.info("Scheduler stopped.")


if __name__ == "__main__":
    run(scheduler())
