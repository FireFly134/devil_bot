import logging
import os
import sys
from typing import Any, Tuple
from urllib.parse import urlparse

from pydantic.v1 import BaseSettings, PostgresDsn, validator

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


class Settings(BaseSettings):
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TESTING: bool = False

    DB_USER: str = "postgres"
    DB_PASSWD: str = "test"
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_NAME: str = "devil_bot"
    DB_URI: PostgresDsn = None

    @validator("DB_NAME", pre=True, allow_reuse=True)
    def get_actual_db_name(cls, v: str | None, values: dict[str, Any]) -> str:
        """Получение названия базы, для тестов генерит отдельное название."""
        if values.get("TESTING") and not v.endswith("_test"):
            v += "_test"
        return v

    @validator("DB_URI", pre=True, allow_reuse=True)
    def assemble_db_connection(
        cls, v: str | None, values: dict[str, Any]
    ) -> str:
        """
        Собираем коннект для подключения к БД.

        :param v: value
        :param values: Dict values
        :return: PostgresDsn
        """
        if isinstance(v, str):
            conn = urlparse(v)
            return PostgresDsn.build(
                scheme=conn.scheme,
                user=conn.username,
                password=conn.password,
                host=conn.hostname,
                port=str(conn.port),
                path=conn.path,
            )

        return PostgresDsn.build(
            scheme="postgresql",
            user=values["DB_USER"],
            password=values["DB_PASSWD"],
            host=values["DB_HOST"],
            port=str(values["DB_PORT"]),
            path=f"/{values['DB_NAME']}",
        )

    TOKEN: str = ""
    stop_word: Tuple[str, str, str] = ("stop", "стоп", "отмена")
    MY_TG_ID: str = ""
    # для VK.com
    ACCESS_TOKEN: str = ""
    DOMAIN: str = ""

    MAX_COUNT_ROCKS: int = 600


settings = Settings(_env_file="../.env")
