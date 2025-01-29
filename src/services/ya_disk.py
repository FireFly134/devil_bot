"""Файл для работы с яндекс-диском."""
import yadisk

from config import settings


class YaDisk:
    """Класс для работы с Yandex Disk."""

    def __init__(self) -> None:
        """Инициализация объекта для работы с Yandex Disk."""
        self.client = yadisk.AsyncClient(token=settings.YANDEX_TOKEN)
        self.root_dir = settings.YANDEX_ROOT_DIR

    async def get_link_on_files(self, path: str) -> str:
        """Получить ссылку на загруженный файл."""
        return await self.client.get_download_link(self.root_dir + path)
