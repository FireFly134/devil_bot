from aiogram import F
from aiogram.enums import ParseMode
from aiogram.types import Message

from menu.menu_help import get_text
from src import form_router
from src.menu.text_menu import menu_useful_information


@form_router.message(F.text == menu_useful_information["for_new_gamers"])
async def for_new_gamers(message: Message) -> None:
    """Для новых игроков."""
    with open(working_folder + "help/manual_for_new_gamers.pdf", "rb") as pdf:
        await message.answer_document(document=pdf)
    text = await get_text("For_new_gamers")
    await message.answer(text, parse_mode=ParseMode.MARKDOWN_V2)


@form_router.message(
    F.text == menu_useful_information["how_to_log_in_to_the_game"]
)
async def how_to_log_in_to_the_game(message: Message) -> None:
    """Как зайти в игру, если по каким-то причинам не получается зайти."""
    await message.answer(
        "https://telegra.ph/Kak-zajti-v-igru-esli-po-kakim-to-prichinam-ne-poluchaetsya-zajti-07-22-3",
    )


@form_router.message(
    F.text == menu_useful_information["who_to_download_at_the_beginning"]
)
async def who_to_download_at_the_beginning(message: Message) -> None:
    """Кого качать в начале."""
    await message.answer(
        "По данному вопросу zOrg написал [статью](https://telegra.ph/Nachalnyj-pak-11-17)\, вот держи\!\)",
        ParseMode.MARKDOWN_V2,
    )


@form_router.message(
    F.text == menu_useful_information["necessary_heroes_for_events"]
)
async def necessary_heroes_for_events(message: Message) -> None:
    """Необходимые герои для ивентов."""
    file_name = {
        "All_Event_Overviews_5_LQ.png": "Все герои из событий.",
        "Sandariel-Event.png": "Сандариэль.",
        "Magnus-Event_Pass.png": "Магнус.",
        "Balthazar-Event.png": "Бальтазар.",
        "Gobliana-Event.png": "Гоблушка.",
        "zigfrid.jpg": "Зигфрид.",
        "Daghan.jpg": "Да'Гана.",
        "ivent_AOM.jpg": "структурированный гайд от Pulcho.",
        "Infographic_Events-1.png": "гайд по событиям.",
    }
    for name in file_name:
        await message.answer("Функции пока что нет.")
        with open(
            working_folder + f"help/necessary_heroes_for_events/{name}", "rb"
        ) as img:
            await message.answer_photo(photo=img, caption=file_name[name])


@form_router.message(F.text == menu_useful_information["useful_links"])
async def useful_links(message: Message) -> None:
    """Полезные ссылки."""
    text = await get_text("Useful_links")
    await message.answer(text, ParseMode.MARKDOWN_V2)


@form_router.message(F.text == menu_useful_information["instructions_for_kv"])
async def instructions_for_kv(message: Message) -> None:
    """Инструкция по КВ."""
    text1 = await get_text("kv1")
    text2 = await get_text("kv2")
    await message.answer(text1)
    await message.answer_photo(
        photo=open(working_folder + "help/kv.jpg", "rb"),
    )
    await message.answer(text2)


@form_router.message(
    F.text == menu_useful_information["instructions_aptechkam_kv"]
)
async def instructions_aptechkam_kv(message: Message) -> None:
    """Гайд по аптечкам в КВ."""
    with open(working_folder + "help/Manual_KV.doc", "rb") as file:
        await message.answer_document(document=file)


@form_router.message(
    F.text == menu_useful_information["packs_and_counterattacks"]
)
async def packs_and_counterattacks(message: Message) -> None:
    """Паки и контрпаки."""
    for name in [
        "pak_and_counterpak1",
        "pak_and_counterpak2",
        "pak_and_counterpak3",
        "pak_and_counterpak4",
        "pak_and_counterpak5",
    ]:
        with open(working_folder + f"help/{name}.jpg", "rb") as img:
            await message.answer_photo(photo=img)


@form_router.message(F.text == menu_useful_information["three_star_trials"])
async def three_star_trials(message: Message) -> None:
    """Испытания на 3*."""
    with open(working_folder + "help/recent_trials.doc", "rb") as doc:
        await message.answer_document(document=doc)


@form_router.message(F.text == menu_useful_information["schemes_of_all_raids"])
async def schemes_of_all_raids(message: Message) -> None:
    """Схемы всех рейдов."""
    await message.answer(
        "[Схемы всех рейдов](https://drive.google.com/folderview?id=1-9P7YK6He09vgheEQd4rK5zf-H5QXDFi)\n\n[Схемы всех рейдов от 🔥 Li \[Феникс\]](https://telegra.ph/Shemy-rejdov-05-19)",
        ParseMode.MARKDOWN_V2,
    )


@form_router.message(
    F.text == menu_useful_information["schedule_of_clan_tasks"]
)
async def schedule_of_clan_tasks(message: Message) -> None:
    """Расписание клановых заданий."""
    await message.answer(await get_text("schedule_of_clan_tasks"))
