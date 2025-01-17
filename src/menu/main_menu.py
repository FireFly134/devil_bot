from datetime import datetime, timedelta
from random import randint

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import settings
from menu.buttons import (
    help_my_button,
    new_button,
    setting_button,
    useful_info_button,
)
from src import SettingProfile, form_router
from src.menu.text_menu import go_back, main_menu
from tables.heroes_of_users import HeroesOfUsers
from tables.telegram_users import User


async def print_rock(message: Message, hero: HeroesOfUsers) -> None:
    """Вывод камней"""
    hours = hero.time_change_kz
    now = datetime.now()
    time1 = timedelta(
        days=now.day, hours=now.hour, minutes=now.minute, seconds=now.second
    )
    time2 = timedelta(
        days=now.day, hours=hours, minutes=30, seconds=0
    )  # noqa: WPS432
    time3 = time2 - time1
    if time3.days == -1:
        time2 = time2 + timedelta(days=1)
        time3 = time2 - time1
    if hero.rock == 0:
        sms = "Ты еще не вводил количество своих камней. Введи количество цифрами!"
    else:
        sms = (
            f'У твоего героя под ником "{hero.name}" - "{hero.rock}" камней! '
            f"Осталось добить {settings.MAX_COUNT_ROCKS - hero.rock}. "
            f"До обновления К.З. осталось {time3}"
        )
    await message.answer(sms)


@form_router.message(F.text == main_menu["help"])
async def helper(message: Message) -> None:
    await help_my_button(message, "Вот, листай список, выбирай!")


@form_router.message(F.text == main_menu["2"])
async def start_print_rock(message: Message) -> None:
    # TODO heroes = await get_heroes_from_user_id(message.from_user.id)
    heroes = (
        await HeroesOfUsers.join(User, HeroesOfUsers.user_id == User.id)
        .select()
        .where(User.user_id == message.from_user.id)
        .with_only_columns(HeroesOfUsers)
        .gino.all()
    )
    keyboard = []
    if len(heroes) == 1:
        await print_rock(message, heroes[0])
    else:
        for hero in heroes:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        text=str(hero.name),
                        callback_data=f"print-{hero.id}",
                    )
                ]
            )
        await message.answer(
            "Кто тебя интересует?",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
        )


@form_router.message(F.text == main_menu["useful_information"])
async def useful_information(message: Message) -> None:
    await useful_info_button(message, "Вот, листай список, выбирай!")


@form_router.message(F.text == main_menu["4"])
async def setting_up_a_profile(message: Message, state: FSMContext) -> None:
    user = await User.query.where(
        User.user_id == message.from_user.id
    ).gino.first()
    info = await HeroesOfUsers.query.where(
        HeroesOfUsers.user_id == user.id
    ).gino.all()
    if len(info) == 1:
        await state.update_data(hero_id=info[0].id)
        await state.update_data(user_id=info[0].user_id)
        await state.update_data(lvel=0)
        await state.set_state(SettingProfile.is_active)

        await setting_button(message, "Что будем изменять?")
    else:
        keyboard = []
        for i in range(len(info)):
            keyboard += [
                [
                    InlineKeyboardButton(
                        text=str(info.name),
                        callback_data=f"setting_profile-{info.id}",
                    )
                ]
            ]
        await message.answer(
            "Выберите, какого героя будем редактировать.",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


@form_router.message(F.text == main_menu["5"])
async def donation_to_my_creator(message: Message) -> None:
    rand_num = randint(1, 15)
    if rand_num == 1:
        await message.answer(
            "Мне на жилье, на большой и просторный сервер😇",
        )
    elif rand_num == 2:
        await message.answer(
            "Моему созадтелю на кофе☕️",
        )
    elif rand_num == 3:
        await message.answer(
            "Моему созадтелю на еду🍲️",
        )
    elif rand_num == 4:
        await message.answer(
            "Моему созадтелю на еду🍺😈",
        )
    elif rand_num == 5:
        await message.answer_sticker(
            sticker="CAACAgIAAxkBAAEIdXBkLGI0l7SBevxq54AYDfwqgrRUAAOwDQAC4mD4SPhHhqikFBgNLwQ",
        )
    elif rand_num == 6:
        await message.answer_sticker(
            sticker="CAACAgIAAxkBAAEIdXJkLGJcvt8bKENug5F9C3b8lLUC8gACuQsAAsqaoUkN2KXU8e7Say8E",
        )
    elif rand_num == 7:
        await message.answer_sticker(
            sticker="CAACAgIAAxkBAAEIdXRkLGJ2W6EizKHiIMyMpQvRhSfxUgACSBMAAt2FmElzhpwNSO5yBy8E",
        )
    elif rand_num == 8:
        await message.answer_sticker(
            sticker="CAACAgIAAxkBAAEIdXZkLGKYqURjcg-n55R5to5rxaAcyQACnwoAApNloUnjCXxz3frjTi8E",
        )
    elif rand_num == 9:
        await message.answer_sticker(
            sticker="CAACAgIAAxkBAAEIdXhkLGKn4-BH-6ihPjj4YlPIhaumAwACIQsAAjooAUkWkfFshXQHLi8E",
        )
    elif rand_num == 10:
        await message.answer_sticker(
            sticker="CAACAgIAAxkBAAEIdXpkLGLSR9RNFUtB6SNh5SJN5GIWYAACTwsAAs4XAAFJ4ud9u0yjrhgvBA",
        )
    elif rand_num == 11:
        await message.answer_sticker(
            sticker="CAACAgIAAxkBAAEIdX9kLGLwylwuMSwGj_kXkWcU_SPb9QACwRQAAqUqCUhsSHVuhH-2XC8E",
        )
    elif rand_num == 12:
        await message.answer_sticker(
            sticker="CAACAgIAAxkBAAEIdYFkLGMILgAB7VKOrsNO5eS3qrtzps0AAl0oAALZEiFKDZLyZ6WHRZMvBA",
        )
    elif rand_num == 13:
        await message.answer_sticker(
            sticker="CAACAgIAAxkBAAEIdYNkLGMcwyMEgf3qBdt6X6T3ey4-QQACaAsAAtv7OUnL_oTTDlslMi8E",
        )
    elif rand_num == 14:
        await message.answer_sticker(
            sticker="CAACAgQAAxkBAAEIdYdkLGQWkK6dqfhrxqQo53zEuqSqHAAC5gsAAk8cWVNQLKJXQdhgTi8E",
        )
    elif rand_num == 15:
        await message.answer_sticker(
            sticker="CAACAgQAAxkBAAEIdYlkLGQat8x1t7j2NPJ01vge-ixN7QACxQwAAplx6FAZ8I5wA_llpi8E",
        )
    # keyboard = [[InlineKeyboardButton("Ссылка на пожертвование через сайт Тинькофф", url='https://www.tinkoff.ru/rm/tkachev.konstantin69/3j6lJ87953')]]
    # with open(working_folder + "QR-code.jpg", "rb") as img:
    # context.bot.send_photo(chat_id=update.effective_chat.id, photo=img, caption="QR\\-код на пожертвование через сайт Тинькофф", parse_mode='MarkdownV2', reply_markup=InlineKeyboardMarkup(keyboard))
    # "[Создатель бота](https://t.me/Menace134) \\- Константин Т\\.", parse_mode='MarkdownV2'
    # context.bot.send_message(chat_id=update.effective_chat.id, text='Отсканируйте QR-код или просто нажмите на ссылку, чтобы отблагодарить автора.')
    await message.answer(
        "СБП по номеру только(Сбер, Газпром, ВТБ, МТС), это временно... @menace134",
    )


@form_router.message(F.text == go_back)
async def go_back(message: Message) -> None:
    # if user_triger[user_id]["setting_hero"]:
    #     buttons.setting_button(
    #         update, context, "Ок, вернулись."
    #     )
    #     user_triger[user_id]["setting_hero"] = False
    # else:
    await new_button(
        message,
        "Погнали назад - в главное меню.",
    )
