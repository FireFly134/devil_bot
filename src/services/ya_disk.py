import io
from typing import BinaryIO

import yadisk
import aiofiles
import asyncio

from config import settings


class YaDisk:
    def __init__(self):
        self.client = yadisk.AsyncClient(token=settings.YANDEX_TOKEN)
        self.root_dir = settings.YANDEX_ROOT_DIR

    async def get_files(self) -> BinaryIO:
        """Получить файл"""
        async with self.client:
            file_stream = io.BytesIO()
            await self.client.download(self.root_dir+"/help/ivent.jpg", file_stream)
        return file_stream

async def main():
    client = YaDisk()
