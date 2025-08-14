"""Модуль для парсинга каналов через Telethon."""
import asyncio
import logging
import re
from typing import Awaitable, Callable, Dict, List, Optional

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.types import (
    BufferedInputFile,
    InputMediaDocument,
    InputMediaPhoto,
)
from sqlalchemy import and_
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.types import Message

from config import settings
from migrations import run_connection_db
from tables.clans import Clans

logger = logging.getLogger(__name__)


class ChannelParser:
    """Парсер каналов Telegram с интеграцией aiogram бота."""

    def __init__(
        self,
        api_id: int,
        api_hash: str,
        bot_token: str,
        session_name: str = "parser",
    ):
        # Используем StringSession из .env если задана
        if getattr(settings, "TELETHON_SESSION", ""):
            self.client = TelegramClient(
                StringSession(settings.TELETHON_SESSION), api_id, api_hash
            )
        else:
            # Файловая сессия (parser.session). Требует предварительной авторизации вне контейнера.
            self.client = TelegramClient(session_name, api_id, api_hash)
        self.bot = Bot(
            token=bot_token,
            session=AiohttpSession(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        self.is_running = False
        # Для хранения медиа-групп
        self.media_groups: Dict[int, List[Message]] = {}
        self.group_timers: Dict[int, asyncio.Task] = {}

        # Карта типов медиа к методам aiogram и имени параметра с файлом
        self._media_send_map: Dict[str, tuple[str, str, str]] = {
            "photo": ("send_photo", "photo", "photo.jpg"),
            "gif": ("send_animation", "animation", "animation.gif"),
            "video": ("send_video", "video", "video.mp4"),
            "document": ("send_document", "document", "document"),
        }

    async def _get_clans(self) -> list[Clans]:
        """Получение кланов, у которых включено получение новостей."""
        return await Clans.query.where(
            and_(
                Clans.news,
                Clans.start,
            )
        ).gino.all()

    async def start(self) -> None:
        """Запуск парсера и бота."""
        await self.client.connect()
        # Ранняя проверка авторизации, чтобы не падать глубоко в run_until_disconnected
        try:
            if not await self.client.is_user_authorized():
                raise RuntimeError(
                    "Telethon не авторизован. Укажите TELETHON_SESSION в .env (StringSession) или заранее авторизуйте файловую сессию parser.session."
                )
        except Exception as auth_err:
            await self.client.disconnect()
            await self.bot.session.close()
            logger.error(f"Auth check failed: {auth_err}")
            raise
        self.is_running = True
        logger.info("Channel parser started")

    async def stop(self) -> None:
        """Остановка парсера и бота."""
        if self.is_running:
            await self.client.disconnect()
            await self.bot.session.close()
            self.is_running = False
            logger.info("Channel parser stopped")

    async def add_channel_handler(self, channel_username: str):
        """Добавить обработчик для канала."""
        try:
            entity = await self.client.get_entity(channel_username)
            logger.info(f"Found channel: {entity.title}")
        except Exception as e:
            logger.error(f"Cannot find channel {channel_username}: {e}")
            return

        @self.client.on(events.NewMessage(chats=[entity]))
        async def handler(event):
            await self._handle_message(event.message)

        logger.info(f"Handler added for channel: {channel_username}")

    async def _handle_message(self, message: Message):
        """Обработка входящего сообщения с поддержкой медиа-групп."""
        # Проверяем, есть ли grouped_id (медиа-группа)
        if message.grouped_id:
            await self._handle_media_group(message)
        else:
            # Обычное сообщение
            await self._forward_message(message)

    async def _handle_media_group(self, message: Message):
        """Обработка медиа-группы."""
        group_id = message.grouped_id

        # Добавляем сообщение в группу
        if group_id not in self.media_groups:
            self.media_groups[group_id] = []

        self.media_groups[group_id].append(message)

        # Отменяем предыдущий таймер для этой группы
        if group_id in self.group_timers:
            self.group_timers[group_id].cancel()

        # Устанавливаем новый таймер на 2 секунды
        self.group_timers[group_id] = asyncio.create_task(
            self._process_media_group_delayed(group_id)
        )

    async def _process_media_group_delayed(self, group_id: int):
        """Обработка медиа-группы с задержкой."""
        await asyncio.sleep(2)  # Ждем 2 секунды для сбора всех медиа

        if group_id in self.media_groups:
            messages = self.media_groups[group_id]
            await self._send_media_group(messages)

            # Очищаем данные группы
            del self.media_groups[group_id]
            if group_id in self.group_timers:
                del self.group_timers[group_id]

    async def _send_media_group(self, messages: List[Message]):
        """Отправка медиа-группы."""
        try:
            media_list = []
            caption_text = ""

            for i, message in enumerate(messages):
                if message.text and not caption_text:
                    caption_text = message.text

                if message.media:
                    if hasattr(message.media, "photo"):
                        file_bytes = await self.client.download_media(
                            message.media, file=bytes
                        )
                        photo = BufferedInputFile(
                            file_bytes, filename=f"photo_{i}.jpg"
                        )

                        # Подпись только к первому элементу группы
                        caption = (
                            self._md_to_html(caption_text)
                            if i == 0 and caption_text
                            else None
                        )
                        media_list.append(
                            InputMediaPhoto(media=photo, caption=caption)
                        )

                    elif hasattr(message.media, "document"):
                        file_bytes = await self.client.download_media(
                            message.media, file=bytes
                        )
                        filename = getattr(
                            message.media.document,
                            "file_name",
                            f"document_{i}",
                        )
                        if not filename:
                            filename = f"document_{i}"

                        document = BufferedInputFile(
                            file_bytes, filename=filename
                        )
                        caption = (
                            self._md_to_html(caption_text)
                            if i == 0 and caption_text
                            else None
                        )
                        media_list.append(
                            InputMediaDocument(media=document, caption=caption)
                        )

            if media_list:
                await self._broadcast_to_clans(
                    lambda clan: self._send_media_group_to_clan(
                        clan, media_list
                    ),
                    description=f"media group x{len(media_list)}",
                )

        except Exception as e:
            logger.error(f"Error forwarding media group: {e}")

    async def _send_media_group_to_clan(self, clan: Clans, media_list: List):
        """Отправка медиа-группы в конкретный клан."""
        try:
            await self.bot.send_media_group(
                chat_id=clan.chat_id,
                media=media_list,
                message_thread_id=clan.thread_id,
            )
            logger.info(
                f"Media group sent to clan {clan.name_clan} ({clan.chat_id})"
            )
        except Exception as e:
            logger.error(
                f"Error sending media group to clan {clan.name_clan}: {e}"
            )

    async def _get_media_file(
        self, message: Message, defaults_file_name: str = "document"
    ) -> BufferedInputFile:
        # Отправляем документ
        file_bytes = await self.client.download_media(
            message.media, file=bytes
        )
        # Получаем имя файла из атрибутов документа
        filename = getattr(message.file, "name", defaults_file_name)

        return BufferedInputFile(file_bytes, filename=filename)

    async def _broadcast_to_clans(
        self,
        send_to_clan: Callable[[Clans], Awaitable[None]],
        description: str,
    ) -> None:
        """Широковещательная отправка в активные кланы.

        Аргумент `send_to_clan` — корутина, отправляющая сообщение в конкретный клан.
        """
        clans = await self._get_clans()
        if not clans:
            logger.info("No active clans to broadcast")
            return
        tasks = [asyncio.create_task(send_to_clan(clan)) for clan in clans]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        errors = [r for r in results if isinstance(r, Exception)]
        if errors:
            logger.warning(
                f"Broadcast '{description}' completed with {len(errors)} errors across {len(clans)} clans"
            )
        else:
            logger.info(
                f"Broadcast '{description}' sent to {len(clans)} clans"
            )

    def _detect_media_kind(self, message: Message) -> Optional[str]:
        """Определение типа медиа в сообщении Telethon."""
        if not message or not message.media:
            return None
        if hasattr(message.media, "photo"):
            return "photo"
        if hasattr(message.media, "gif"):
            return "gif"
        if hasattr(message.media, "video"):
            return "video"
        if hasattr(message.media, "document"):
            return "document"
        return None

    async def _send_single_media_to_clan(
        self, clan: Clans, message: Message, caption: str
    ) -> None:
        """Единая отправка одного медиа-сообщения в клан на основе карты методов."""
        kind = self._detect_media_kind(message)
        if not kind:
            return
        method_name, file_kwarg, default_name = self._media_send_map[kind]
        file_obj = await self._get_media_file(message, default_name)
        method = getattr(self.bot, method_name)
        kwargs = {
            "chat_id": clan.chat_id,
            file_kwarg: file_obj,
            "caption": caption,
            "message_thread_id": clan.thread_id,
        }
        # Для документа caption может отсутствовать, но aiogram допускает
        await method(**kwargs)
        logger.info(f"{kind.capitalize()} sent to clan {clan.name_clan}")

    async def _forward_message(self, message: Message):
        """Пересылка сообщения через aiogram бота."""
        try:
            # Получаем текст сообщения
            text = message.text or ""
            text_html = self._md_to_html(text) if text else ""

            # Медиа-сообщение
            if message.media and self._detect_media_kind(message):
                await self._broadcast_to_clans(
                    lambda clan: self._send_single_media_to_clan(
                        clan, message, text_html
                    ),
                    description="single media",
                )
                return

            # Обычное текстовое сообщение
            if text_html:
                await self._broadcast_to_clans(
                    lambda clan: self.bot.send_message(
                        chat_id=clan.chat_id,
                        text=text_html,
                        message_thread_id=clan.thread_id,
                    ),
                    description="text",
                )

        except Exception as e:
            logger.error(f"Error forwarding message: {e}")

    def _md_to_html(self, text: str) -> str:
        """Конвертирует упрощённый Markdown (**, __, _, []()) в HTML для Telegram HTML parse_mode."""
        if not text:
            return text

        # Экранирование HTML-символов
        escaped = (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        # Ссылки [text](url)
        escaped = re.sub(
            r"\[([^\]]*)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped
        )

        # Жирный **text**
        escaped = re.sub(
            r"\*\*(.+?)\*\*", lambda m: f"<b>{m.group(1)}</b>", escaped
        )

        # Курсив __text__
        escaped = re.sub(
            r"__([^_]+?)__", lambda m: f"<i>{m.group(1)}</i>", escaped
        )

        # Подчеркнутый _text_
        escaped = re.sub(
            r"(?<!_)_(?!_)(.+?)(?<!_)_(?!_)",
            lambda m: f"<u>{m.group(1)}</u>",
            escaped,
        )

        return escaped

    async def run_until_disconnected(self) -> None:
        """Запуск в бесконечном цикле."""
        await self.client.run_until_disconnected()


async def main():
    """Основная функция для тестирования парсера."""
    # Инициализируем подключение к БД
    await run_connection_db()

    parser = ChannelParser(
        api_id=int(settings.API_ID),
        api_hash=settings.API_HASH,
        bot_token=settings.TOKEN,
    )

    try:
        await parser.start()
        await parser.add_channel_handler(
            channel_username=settings.CHANNEL_USERNAME
        )
        await parser.run_until_disconnected()
    finally:
        await parser.stop()


if __name__ == "__main__":
    asyncio.run(main())
