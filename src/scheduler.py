"""Файл для запуска планировщика."""
import logging
from asyncio import Future, run

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

from src.request import main as get_news

# from src.reminder import main as reminder
# from src.reminder_events import main as reminder_events


async def scheduler() -> None:
    """Запуск планировщика."""

    logging.info("Scheduler starting...")
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        get_news,
        "cron",
        id="get_news",
        minute="*/5",
        timezone=timezone("Europe/Moscow"),
        replace_existing=True,
    )
    # scheduler.add_job(
    #     reminder,
    #     "cron",
    #     id="reminder",
    #     minute=[0,30],
    #     timezone=timezone("Europe/Moscow"),
    #     replace_existing=True,
    # )
    # scheduler.add_job(
    #     reminder_events,
    #     "cron",
    #     id="reminder_events",
    #     hour="12",
    #     minute="0",
    #     timezone=timezone("Europe/Moscow"),
    #     replace_existing=True,
    # )
    logging.info("added tasks to cron scheduler")
    scheduler.start()
    try:
        await Future()  # Держим планировщик запущенным
    except (KeyboardInterrupt, SystemExit):
        pass  # Нормальное завершение
    finally:
        scheduler.shutdown()
        logging.info("Scheduler stopped.")


if __name__ == "__main__":
    run(scheduler())
