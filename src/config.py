import logging
import sys
from typing import Tuple

from pydantic_settings import BaseSettings

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


class Settings(BaseSettings):
    DB_USER: str = "postgres"
    DB_PASSWD: str = "test"
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_NAME: str = "test_bot"

    TOKEN: str = ""
    stop_word: Tuple[str, str, str] = ("stop", "стоп", "отмена")
    MY_TG_ID: str = ""
    # для VK.com
    ACCESS_TOKEN: str = ""
    DOMAIN: str = ""


settings = Settings(_env_file="../.env")

DB_URI: str = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
