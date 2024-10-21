from aiogram.types import (
    FSInputFile,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from menu.text_menu import go_back, main_menu, menu_help
from migrations import db
from tables.heroes_of_users import HeroesOfUsers


async def send_message(
    message: Message, sms: str, reply_keyboard: list[list[KeyboardButton]]
) -> None:
    await message.answer(
        sms,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=False,
        ),
    )


async def setting_button(message: Message, sms: str) -> None:
    """Вывод кнопок Настроек"""
    reply_keyboard = [
        [KeyboardButton(text="Манипуляции с героем")],
        [
            KeyboardButton(text="Подписки..."),
            KeyboardButton(text="Поменять время..."),
        ],
        [KeyboardButton(text="Проверить данные профиля")],
        [KeyboardButton(text=go_back)],
    ]
    await send_message(message, sms, reply_keyboard)


async def setting_hero_button(
    message: Message, user_id: int, sms: str
) -> None:
    """Манапуляции с героем"""
    reply_keyboard = []
    num = await db.func.count(HeroesOfUsers.user_id == user_id).gino.scalar()
    #     pd.read_sql(
    #     f"SELECT COUNT(*) FROM heroes_of_users WHERE user_id = '{update.effective_chat.id}';",
    #     engine,
    # ))
    # num = int(info.loc[0, "count"])
    if num == 5:
        reply_keyboard += [
            [KeyboardButton(text="Удалить одного героя")],
            [KeyboardButton(text="Переименовать героя")],
            [KeyboardButton(text=go_back)],
        ]
    elif num == 1:
        reply_keyboard += [
            [KeyboardButton(text="Добавить еще одного героя")],
            [KeyboardButton(text="Переименовать героя")],
            [KeyboardButton(text=go_back)],
        ]
    else:
        reply_keyboard += [
            [KeyboardButton(text="Добавить еще одного героя")],
            [KeyboardButton(text="Удалить одного героя")],
            [KeyboardButton(text="Переименовать героя")],
            [KeyboardButton(text=go_back)],
        ]
    await send_message(message, sms, reply_keyboard)


async def subscription_button(
    message: Message, sms: str, id_hero: str
) -> None:
    """Подписки..."""

    subscription = HeroesOfUsers.query.where(
        HeroesOfUsers.id == id_hero
    ).first()
    # subscription = pd.read_sql(
    #     f"SELECT subscription_rock, subscription_energy, description_of_the_kz FROM heroes_of_users WHERE user_id = '{update.effective_chat.id}' AND id = '{id_hero}';",
    #     engine,
    # )
    reply_keyboard = []
    if subscription.subscription_rock:
        reply_keyboard += [
            [
                KeyboardButton(
                    text="Отписаться от напоминалки о смене КЗ за час"
                )
            ]
        ]
    else:
        reply_keyboard += [
            [
                KeyboardButton(
                    text="Подписаться на напоминалку о смене КЗ за час"
                )
            ]
        ]
    if subscription.subscription_energy:
        reply_keyboard += [
            [KeyboardButton(text="Отписаться от напоминалки по сбору энергии")]
        ]
    else:
        reply_keyboard += [
            [
                KeyboardButton(
                    text="Подписаться на напоминалку по сбору энергии"
                )
            ]
        ]
    if subscription.description_of_the_kz:
        reply_keyboard += [
            [KeyboardButton(text="Отписаться от ежедневного описания КЗ")]
        ]
    else:
        reply_keyboard += [
            [KeyboardButton(text="Подписаться на ежедневное описание КЗ")]
        ]
    reply_keyboard += [[KeyboardButton(text=go_back)]]
    await send_message(message, sms, reply_keyboard)


async def edit_time_button(message: Message, sms: str) -> None:
    """Поменять время..."""
    reply_keyboard = [
        [KeyboardButton(text="Поменять время смены КЗ")],
        [KeyboardButton(text="Поменять время первого сбора энергии")],
        [KeyboardButton(text=go_back)],
    ]
    await send_message(message, sms, reply_keyboard)


async def new_button(message: Message, sms: str) -> None:
    """Вывод кнопок"""
    reply_keyboard = [
        [KeyboardButton(text=main_menu["1"])],
        [
            KeyboardButton(text=main_menu["2"]),
            KeyboardButton(text=main_menu["3"]),
        ],
        [KeyboardButton(text=main_menu["4"])],
        [KeyboardButton(text=main_menu["5"])],
    ]
    # TODO будут ли у нас Админы?
    # info = pd.read_sql(
    #     f"SELECT COUNT(*) FROM admins WHERE user_id = '{update.effective_chat.id}';",
    #     engine,
    # )
    # if info.loc[0, "count"] != 0:
    #     reply_keyboard += [[KeyboardButton(text="Настройки Админа")]]
    await send_message(message, sms, reply_keyboard)


async def setting_admin_button(message: Message, sms: str) -> None:
    """Вывод кнопок админовских настроек"""
    reply_keyboard = [
        [
            KeyboardButton(text="Отправить напоминалку игроку ✏️✉️🧍‍♂️"),
            KeyboardButton(text="Редактировать сообщение напоминалки 📝"),
            KeyboardButton(text="Написать от имени бота🤖"),
        ],
        [
            KeyboardButton(text="Отправить ВСЕМ сообщение ✏️✉️👨‍👩‍👧‍👦"),
            KeyboardButton(text="Убрать игрока из клана☠"),
        ],
        [KeyboardButton(text=go_back)],
    ]
    await send_message(message, sms, reply_keyboard)


async def help_my_button(message: Message, sms: str) -> None:
    """Вывод кнопок помощи"""
    reply_keyboard = [
        [KeyboardButton(text=menu_help["instructions_for_use"])],
        [
            KeyboardButton(
                text=menu_help[
                    "instructions_for_implementing_the_bot_in_the_chat"
                ]
            )
        ],
        [KeyboardButton(text=menu_help["basic_commands_in_the_chat"])],
        [KeyboardButton(text=go_back)],
    ]
    await send_message(message, sms, reply_keyboard)


async def useful_info_button(message: Message, sms: str) -> None:
    """Вывод кнопок помощи"""
    reply_keyboard = [
        [KeyboardButton(text="Для новичков")],
        [
            KeyboardButton(
                text="Как зайти в игру, если по каким-то причинам не получается зайти"
            )
        ],
        [
            KeyboardButton(text="Кого качать в начале"),
            KeyboardButton(
                text="Кого качать для получения героев из событий?"
            ),
        ],
        [KeyboardButton(text="Полезные ссылки")],
        [
            KeyboardButton(text="Инструкция по КВ"),
            KeyboardButton(text="Гайд по аптечкам в КВ"),
        ],
        [
            KeyboardButton(text="Паки и контрпаки"),
            KeyboardButton(text="Испытания на 3*"),
        ],
        [KeyboardButton(text="Схемы всех рейдов")],
        [KeyboardButton(text="Расписание клановых заданий")],
        [KeyboardButton(text=go_back)],
    ]
    await send_message(message, sms, reply_keyboard)


async def cancel_button(message: Message, sms: str) -> None:
    """Кнопка отмены"""
    await send_message(message, sms, [[KeyboardButton(text="Отмена")]])
