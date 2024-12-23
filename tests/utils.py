"""Модуль с инструментами для тестов."""
from contextlib import contextmanager

from sqlalchemy_utils import create_database, drop_database
from sqlalchemy_utils.functions import database_exists
from yarl import URL

from src.config import settings


@contextmanager
def get_tmp_database(**kwargs: dict) -> str:
    """Создать временную бд для тестов."""
    if kwargs.get("template"):
        db_url = URL(settings.DB_URI).path.replace("_template_", "_test_")
    else:
        db_url = URL(settings.DB_URI).path.replace("_test_", "_template_")

    tmp_db_url = str(URL(settings.DB_URI).with_path(db_url))

    if database_exists(tmp_db_url):
        drop_database(tmp_db_url)
    create_database(tmp_db_url, **kwargs)
    try:
        yield tmp_db_url
    finally:
        if database_exists(tmp_db_url):
            drop_database(tmp_db_url)
