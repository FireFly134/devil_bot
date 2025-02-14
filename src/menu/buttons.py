from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from menu.text_menu import (
    cancel,
    go_back,
    main_menu,
    menu_help,
    menu_useful_information,
    setting_profile,
)
from migrations import db
from tables.heroes_of_users import HeroesOfUsers
from tables.telegram_users import User


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
        [KeyboardButton(text=setting_profile["setting_hero"])],
        [
            KeyboardButton(text=setting_profile["subscribe"]),
            KeyboardButton(text=setting_profile["update_time"]),
        ],
        [KeyboardButton(text=setting_profile["show_data_profile"])],
        [KeyboardButton(text=go_back)],
    ]
    await send_message(message, sms, reply_keyboard)


async def setting_hero_button(
    message: Message, user_id: int, sms: str, name: str
) -> None:
    """Манапуляции с героем."""
    reply_keyboard = []
    num = await db.func.count(HeroesOfUsers.user_id == user_id).gino.scalar()
    if num == 5:
        reply_keyboard += [
            [
                KeyboardButton(
                    text=setting_profile["delete_hero"] + f" ({name})"
                )
            ],
            [
                KeyboardButton(
                    text=setting_profile["rename_hero"] + f" ({name})"
                )
            ],
            [KeyboardButton(text=go_back)],
        ]
    elif num == 1:
        reply_keyboard += [
            [KeyboardButton(text=setting_profile["add_hero"])],
            [
                KeyboardButton(
                    text=setting_profile["rename_hero"] + f" ({name})"
                )
            ],
            [KeyboardButton(text=go_back)],
        ]
    else:
        reply_keyboard += [
            [KeyboardButton(text=setting_profile["add_hero"])],
            [
                KeyboardButton(
                    text=setting_profile["delete_hero"] + f" ({name})"
                )
            ],
            [
                KeyboardButton(
                    text=setting_profile["rename_hero"] + f" ({name})"
                )
            ],
            [KeyboardButton(text=go_back)],
        ]
    await send_message(message, sms, reply_keyboard)


async def subscription_button(
    message: Message, sms: str, id_hero: str
) -> None:
    """Подписки..."""

    hero = await HeroesOfUsers.query.where(
        HeroesOfUsers.id == id_hero
    ).gino.first()
    user = await User.query.where(
        User.user_id == message.from_user.id
    ).gino.first()

    reply_keyboard = []
    if hero.subscription_rock:
        reply_keyboard += [
            [KeyboardButton(text=setting_profile["unsubscribe_replace_kz"])]
        ]
    else:
        reply_keyboard += [
            [KeyboardButton(text=setting_profile["subscribe_replace_kz"])]
        ]
    if hero.subscription_energy:
        reply_keyboard += [
            [KeyboardButton(text=setting_profile["unsubscribe_energy"])]
        ]
    else:
        reply_keyboard += [
            [KeyboardButton(text=setting_profile["subscribe_energy"])]
        ]
    if hero.description_of_the_kz:
        reply_keyboard += [
            [
                KeyboardButton(
                    text=setting_profile["unsubscribe_description_kz"]
                )
            ]
        ]
    else:
        reply_keyboard += [
            [KeyboardButton(text=setting_profile["subscribe_description_kz"])]
        ]
    if user.subscription_event:
        reply_keyboard += [
            [KeyboardButton(text=setting_profile["unsubscribe_event"])]
        ]
    else:
        reply_keyboard += [
            [KeyboardButton(text=setting_profile["subscribe_event"])]
        ]
    reply_keyboard += [[KeyboardButton(text=go_back)]]
    await send_message(message, sms, reply_keyboard)


async def edit_time_button(message: Message, sms: str) -> None:
    """Поменять время..."""
    reply_keyboard = [
        [KeyboardButton(text=setting_profile["update_time_replace_kz"])],
        [KeyboardButton(text=setting_profile["update_time_energy"])],
        [KeyboardButton(text=go_back)],
    ]
    await send_message(message, sms, reply_keyboard)


async def new_button(message: Message, sms: str) -> None:
    """Вывод кнопок"""
    reply_keyboard = [
        [KeyboardButton(text=main_menu["help"])],
        [
            KeyboardButton(text=main_menu["2"]),
            KeyboardButton(text=main_menu["useful_information"]),
        ],
        [KeyboardButton(text=main_menu["4"])],
        # [KeyboardButton(text=main_menu["5"])], # noqa: E800
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
    """Вывод кнопок помощи для новых игроков."""
    reply_keyboard = [
        [KeyboardButton(text=menu_useful_information["for_new_gamers"])],
        [
            KeyboardButton(
                text=menu_useful_information["how_to_log_in_to_the_game"]
            )
        ],
        [
            KeyboardButton(
                text=menu_useful_information[
                    "who_to_download_at_the_beginning"
                ]
            ),
            KeyboardButton(
                text=menu_useful_information["necessary_heroes_for_events"]
            ),
        ],
        [KeyboardButton(text=menu_useful_information["useful_links"])],
        [
            KeyboardButton(
                text=menu_useful_information["instructions_for_kv"]
            ),
            KeyboardButton(
                text=menu_useful_information["instructions_aptechkam_kv"]
            ),
        ],
        [
            KeyboardButton(
                text=menu_useful_information["packs_and_counterattacks"]
            ),
            KeyboardButton(text=menu_useful_information["three_star_trials"]),
        ],
        [KeyboardButton(text=menu_useful_information["schemes_of_all_raids"])],
        [
            KeyboardButton(
                text=menu_useful_information["schedule_of_clan_tasks"]
            )
        ],
        [KeyboardButton(text=go_back)],
    ]
    await send_message(message, sms, reply_keyboard)


async def cancel_button(message: Message, sms: str) -> None:
    """Кнопка отмены"""
    await send_message(message, sms, [[KeyboardButton(text=cancel)]])
