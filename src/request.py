import asyncio
import json
import logging
import os.path
import time
from datetime import datetime
from threading import Thread
from typing import Any

import requests
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.handlers import error
from aiogram.types import InputMediaPhoto
from sqlalchemy import and_

from config import settings
from migrations import run_connection_db
from tables.clans import Clans
from tables.post_news import PostNews


class GameNews:
    """Игровые новости"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.url = "https://api.vk.com/method/wall.get"
        self.request_params = {
            "access_token": settings.ACCESS_TOKEN,
            "v": 5.131,
            "domain": settings.DOMAIN,
            "count": 5,
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        }

    async def _get_request_news(self) -> list[dict[str, Any]]:
        """Получение новостей из официальной группы игры, по VK API."""
        r = requests.get(
            self.url,
            headers=self.headers,
            params=self.request_params,
        )

        return r.json()["response"]["items"]

    async def _get_content_news(self) -> list[dict[str, str | int | datetime]]:
        """Получение контента из новостей."""
        posts_list = []
        data = await self._get_request_news()
        last_post_id = await self._get_last_post_id()
        for item in data:
            if item["id"] <= last_post_id:
                continue
            date_pub = datetime.fromtimestamp(item["date"]).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            urls_photo = []
            for i in range(len(item["attachments"])):
                if item["attachments"][i]["type"] == "photo":
                    max_h_val = 0
                    max_w_val = 0
                    url_photo = ""
                    for dist in item["attachments"][i]["photo"]["sizes"]:
                        if dist["height"] > max_h_val:
                            max_h_val = dist["height"]
                            max_w_val = dist["width"]
                            url_photo = dist["url"]
                        elif (
                            dist["height"] == max_h_val
                            and dist["width"] > max_w_val
                        ):
                            max_w_val = dist["width"]
                            url_photo = dist["url"]
                    urls_photo.append(url_photo)
                    posts_list.append(
                        {
                            "id": item["id"],
                            "text": item["text"],
                            "photos": urls_photo,
                            "date_pub": date_pub,
                        }
                    )
        return posts_list

    async def _get_clans(self):
        """Получение кланов, у которых включено получение новостей."""
        return Clans.query.where(
            and_(
                Clans.news,
                Clans.start,
            )
        ).gino.all()

    async def _get_last_post_id(self) -> int:
        """Получение последнего id поста."""
        last_post = await PostNews.query.order_by(
            PostNews.id.desc()
        ).gino.first()
        return last_post.id if last_post else 0

    async def _save_post_info_in_db(self, posts_list: list[dict]):
        """Сохранение информации о постах в БД."""
        for posts in posts_list:
            try:
                await PostNews.create(**posts)
            except Exception as err:
                logging.error(err)
                logging.error(f"Не смог произвести запись в БД. {posts}")

    async def send_news(
        self, posts_list: list[dict], chat_id: str = settings.MY_TG_ID
    ) -> None:
        # TODO Метод отправки постов не готов! :с
        """Отправка новостей в чат."""
        try:
            for post in posts_list:
                media_group = []
                for photo in post["photos"]:
                    if not media_group:
                        media_group.append(
                            InputMediaPhoto(
                                photo,
                                post["text"],
                            )
                        )
                    else:
                        media_group.append(InputMediaPhoto(photo))
                try:
                    await self.bot.send_media_group(
                        chat_id=chat_id, media=media_group
                    )
                except error.BadRequest:
                    media_group[0] = InputMediaPhoto(post["photo"][0])
                    await self.bot.send_media_group(
                        chat_id=chat_id, media=media_group
                    )
                    await self.bot.send_message(
                        chat_id=chat_id, text=post["text"]
                    )
        except Exception as err:
            logging.info(
                f"Ошибка при попытке отправить пост в группу {chat_id}: {err}"
            )

    async def check_news(self) -> None:
        """Проверка новостей."""
        if posts_list := await self._get_content_news():
            await self._save_post_info_in_db(posts_list)
            for clan in await self._get_clans():
                await self.send_news(posts_list, chat_id=clan.chat_id)


async def main() -> None:
    game_news = GameNews(
        Bot(
            token=settings.TOKEN,
            session=AiohttpSession(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
    )
    await run_connection_db()
    # while True:
    try:
        await game_news.check_news()
    except Exception as err:
        logging.info(f"Ошибка при попытке парсинга: {err}")
        # time.sleep(300)


if __name__ == "__main__":
    asyncio.run(main())
