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
from src.services.reminder.reminder_kz import reminder_kz

# from src.services.reminder.reminder_events import main as reminder_events  # noqa: E800


async def scheduler() -> None:
    """Запуск планировщика."""
    logging.info("Scheduler starting...")
    io_scheduler = AsyncIOScheduler()
    io_scheduler.add_job(
        get_news,
        "cron",
        id="get_news",
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
        minute="0",
        timezone=timezone("Europe/Moscow"),
        replace_existing=True,
    )
    io_scheduler.add_job(
        reminder_kz,
        "cron",
        id="reminder_kz",
        minute="30",
        timezone=timezone("Europe/Moscow"),
        replace_existing=True,
    )
    # io_scheduler.add_job(  # noqa: E800
    #     reminder,  # noqa: E800
    #     "cron",  # noqa: E800
    #     id="reminder",  # noqa: E800
    #     minute=[0,30],  # noqa: E800
    #     timezone=timezone("Europe/Moscow"),  # noqa: E800
    #     replace_existing=True,  # noqa: E800
    # )  # noqa: E800
    # io_scheduler.add_job(  # noqa: E800
    #     reminder_events,  # noqa: E800
    #     "cron",  # noqa: E800
    #     id="reminder_events",  # noqa: E800
    #     hour="12",  # noqa: E800
    #     minute="0",  # noqa: E800
    #     timezone=timezone("Europe/Moscow"),  # noqa: E800
    #     replace_existing=True,  # noqa: E800
    # )  # noqa: E800
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
