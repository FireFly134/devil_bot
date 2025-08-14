"""Парсер новостей из официальной группы игры, в VK."""

import asyncio
import logging
from datetime import datetime
from typing import Any

import requests
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InputMediaPhoto
from sqlalchemy import and_

from config import settings
from migrations import run_connection_db
from tables.clans import Clans
from tables.post_news import PostNews


class GameNews:
    """Игровые новости"""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.url = "https://api.vk.com/method/wall.get"
        self.request_params = {
            "access_token": settings.VK_ACCESS_TOKEN,
            "v": 5.131,
            "domain": settings.DOMAIN,
            "count": 5,
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        }

    async def _get_request_news(self) -> list[dict[str, Any]]:
        """Получение новостей из официальной группы игры, по VK API."""
        response = requests.get(
            self.url,
            headers=self.headers,
            params=self.request_params,
        )

        return response.json()["response"]["items"]

    async def _get_content_news(self) -> list[dict[str, str | int | datetime]]:
        """Получение контента из новостей."""
        posts_list = []
        try:
            news = await self._get_request_news()
        except Exception as err:
            logging.info(f"Ошибка при попытке получения новостей: {err}")
            return posts_list
        for post in news:
            if post["id"] <= await self._get_last_post_id():
                continue
            urls_photo = []
            for i in range(len(post["attachments"])):
                if post["attachments"][i]["type"] == "photo":
                    max_h_val = 0
                    max_w_val = 0
                    url_photo = ""
                    for dist in post["attachments"][i]["photo"]["sizes"]:
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
                            "id": post["id"],
                            "text": post["text"],
                            "photos": urls_photo,
                            "date_pub": datetime.fromtimestamp(post["date"]),
                        }
                    )
        return posts_list

    async def _get_clans(self) -> list[Clans]:
        """Получение кланов, у которых включено получение новостей."""
        return await Clans.query.where(
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

    async def build_and_send_news_message(self, post: PostNews) -> None:
        """Сборка сообщений с новостью для отправки в чат."""
        clans: list[Clans] = await self._get_clans()
        tasks = []
        media_group = []
        for photo in post.photos:
            if not media_group:
                media_group.append(
                    InputMediaPhoto(
                        media=photo,
                        caption=post.text,
                    )
                )
            else:
                media_group.append(InputMediaPhoto(media=photo))
        for clan in clans:
            tasks.append(
                asyncio.create_task(
                    self._send_message_news(clan, media_group, post)
                )
            )

        await post.update(is_send=True).apply()
        await asyncio.wait(tasks)

    async def _send_message_news(
        self, clan: Clans, media_group: list[InputMediaPhoto], post: PostNews
    ) -> None:
        """Отправка новостей в чат."""
        try:
            await self.bot.send_media_group(
                chat_id=clan.chat_id,
                media=media_group,
                message_thread_id=clan.thread_id,
            )
        except TelegramBadRequest as err:
            if "message caption is too long" in str(err):
                media_group[0] = InputMediaPhoto(media=post.photos[0])
                await self.bot.send_media_group(
                    chat_id=clan.chat_id,
                    media=media_group,
                    message_thread_id=clan.thread_id,
                )
                await self.bot.send_message(
                    chat_id=clan.chat_id,
                    text=post.text,
                    message_thread_id=clan.thread_id,
                )
            elif "chat not found" in str(err):
                logging.info(
                    f"Ошибка при попытке отправить пост в группу {clan.chat_id}: {err}"
                )
            else:
                logging.info(str(err))

    async def check_news(self) -> None:
        """Проверка новостей."""
        if posts_list := await self._get_content_news():  # noqa: WPS332
            await self._save_post_info_in_db(posts_list)


async def send_news(game_news: GameNews) -> None:
    """Отправка новостей."""
    post = (
        await PostNews.query.where(~PostNews.is_send)
        .order_by(PostNews.id.asc())
        .gino.first()
    )
    if post:
        await game_news.build_and_send_news_message(post)


async def main() -> None:
    """Запуск парсинга новостей."""
    game_news = GameNews(
        Bot(
            token=settings.TOKEN,
            session=AiohttpSession(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
    )
    await run_connection_db()
    await game_news.check_news()
    await send_news(game_news)


if __name__ == "__main__":
    asyncio.run(main())
