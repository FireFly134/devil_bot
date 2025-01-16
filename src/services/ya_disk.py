import os

import yadisk

from config import settings


class YaDisk:
    def __init__(self):
        self.client = yadisk.AsyncClient(token=settings.YANDEX_TOKEN)
        self.root_dir = settings.YANDEX_ROOT_DIR

    async def get_link_on_files(self, path: str) -> str:
        """Получить ссылку на загруженный файл"""
        url = await self.client.get_download_link(self.root_dir + path)
        return url
