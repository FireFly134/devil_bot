import asyncio
import logging
from typing import Any

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.handlers import error
from aiogram.types import InputMediaPhoto
from sqlalchemy import and_

from config import settings

from tables.clans import Clans
import datetime
import json
import logging
import os.path
import time
from threading import Thread

import requests

class GameNews:
    """Игровые новости"""
    def __init__(self, bot:Bot):
        self.bot = bot
        self.url = "https://api.vk.com/method/wall.get"
        self.request_params={
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
        for item in data:
            date_pub = datetime.datetime.fromtimestamp(item["date"]).strftime("%Y-%m-%d")
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
                        elif dist["height"] == max_h_val and dist["width"] > max_w_val:
                            max_w_val = dist["width"]
                            url_photo = dist["url"]
                    urls_photo.append(url_photo)
                posts_list.append(
                    {
                        "id": item["id"],
                        "text": item["text"],
                        "photo": urls_photo,
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

    async def _get_last_post_id(self) -> str:
        """Получение последнего id поста."""
        if os.path.isfile("post_id.txt"):
            with open("post_id.txt", "r") as file:
                post_id = file.read()
        else:
            post_id = "0"
        return post_id

    async def _save_post_info(self, posts_list: list[dict], post_id: str):
        """Сохранение информации о постах."""
        with open("posts_data.json", "w") as file:
            json.dump(
                posts_list, file, indent=4
            )  # ,ensure_ascii=False
        with open("post_id.txt", "w") as file:
            file.write(post_id)

    def send_news(
            self, chat_id: str = settings.MY_TG_ID, num: int = 1
    ) -> None:
        try:
            with open("posts_data.json") as file:
                posts_list = json.load(file)
            media_group = []
            for i in range(len(posts_list[num]["photo"])):
                if media_group == []:
                    media_group.append(
                        InputMediaPhoto(
                            posts_list[num]["photo"][i],
                            posts_list[num]["text"]
                        )
                    )
                else:
                    media_group.append(
                        InputMediaPhoto(
                            posts_list[num]["photo"][i])
                    )
            try:
                await self.bot.send_media_group(chat_id=chat_id, media=media_group)
            except error.BadRequest:
                media_group[0] = InputMediaPhoto(
                    posts_list[num]["photo"][0]
                )
                await self.bot.send_media_group(chat_id=chat_id, media=media_group)
                await self.bot.send_message(chat_id=chat_id,
                                 text=posts_list[num]["text"])
        except Exception as err:
            logging.info(
                f"Ошибка при попытке отправить пост в группу {chat_id}: {err}"
            )

    async def check_news(self) -> None:
        """Проверка новостей."""
        posts_list = await self._get_content_news()
        post_id = await self._get_last_post_id()

        date = "1994-10-07"
        num = 0
        for i in range(len(posts_list)):
            if posts_list[i]["date_pub"] > date:
                date = posts_list[i]["date_pub"]
                num = i
        if str(post_id) != str(posts_list[num]["id"]):
            post_id = str(posts_list[num]["id"])
            await self._save_post_info(posts_list, post_id)

            for clan in await self._get_clans():
                t = Thread(
                    target=self.send_news,
                    args=(
                        clan.chat_id,
                        num,
                    ),
                )
                t.start()
                t.join()

async def main() -> None:
    game_news = GameNews(Bot(
        token=settings.TOKEN,
        session=AiohttpSession(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    ))
    while True:
        try:
            await game_news.check_news()
        except Exception as err:
            logging.info(f"Ошибка при попытке парсинга: {err}")
        time.sleep(300)

if __name__ == "__main__":
    asyncio.run(main())

