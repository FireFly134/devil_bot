import pytest

from services.ya_disk import YaDisk


@pytest.mark.asyncio()
async def test_ya_disk():
    yadisk = YaDisk()
    client = yadisk.client
    # Проверяет, валиден ли токен
    assert await client.check_token()

    # Получает общую информацию о диске
    assert await client.get_disk_info()

    assert [i async for i in client.listdir("/files_for_bot")]
    assert [i async for i in client.listdir("/files_for_bot/help")]
    assert [
        i
        async for i in client.listdir(
            "/files_for_bot/help/necessary_heroes_for_events"
        )
    ]
    client.close()

    assert await yadisk.get_link_on_files("/help/kv.jpg")
