from typing import Any
from unittest.mock import AsyncMock

import pytest

from src.request import GameNews

response = [
    {
        "inner_type": "wall_wallpost",
        "donut": {"is_donut": False},
        "is_pinned": 1,
        "comments": {"can_post": 0, "count": 0, "groups_can_post": True},
        "marked_as_ads": 0,
        "hash": "u3n8zoBH6wor-RYxxg",
        "type": "post",
        "push_subscription": {"is_subscribed": False},
        "carousel_offset": 0,
        "attachments": [
            {
                "type": "photo",
                "photo": {
                    "album_id": -7,
                    "date": 1712151732,
                    "id": 457262940,
                    "owner_id": -149861500,
                    "access_key": "3e1fb8fbaa424a4af8",
                    "post_id": 159823,
                    "sizes": [
                        {
                            "height": 30,
                            "type": "s",
                            "width": 75,
                            "url": "https://sun9-62.userapi.com/s/v1/ig2/DIR_THon0_2NTexNFPyhTBCO5Y7ORAhoealGAxEUXZt27QJyNbdsO7WMX_NvyKVzejJjd9lmzSXV0CLw0Id_-nO4.jpg?quality=95&as=32x13,48x19,72x29,108x43,160x64,240x96,360x144,480x192,540x216,640x256,720x288,800x320&from=bu&cs=75x30",
                        },
                        {
                            "height": 52,
                            "type": "m",
                            "width": 130,
                            "url": "https://sun9-62.userapi.com/s/v1/ig2/DIR_THon0_2NTexNFPyhTBCO5Y7ORAhoealGAxEUXZt27QJyNbdsO7WMX_NvyKVzejJjd9lmzSXV0CLw0Id_-nO4.jpg?quality=95&as=32x13,48x19,72x29,108x43,160x64,240x96,360x144,480x192,540x216,640x256,720x288,800x320&from=bu&cs=130x52",
                        },
                        {
                            "height": 242,
                            "type": "x",
                            "width": 604,
                            "url": "https://sun9-62.userapi.com/s/v1/ig2/DIR_THon0_2NTexNFPyhTBCO5Y7ORAhoealGAxEUXZt27QJyNbdsO7WMX_NvyKVzejJjd9lmzSXV0CLw0Id_-nO4.jpg?quality=95&as=32x13,48x19,72x29,108x43,160x64,240x96,360x144,480x192,540x216,640x256,720x288,800x320&from=bu&cs=604x242",
                        },
                        {
                            "height": 320,
                            "type": "y",
                            "width": 800,
                            "url": "https://sun9-62.userapi.com/s/v1/ig2/DIR_THon0_2NTexNFPyhTBCO5Y7ORAhoealGAxEUXZt27QJyNbdsO7WMX_NvyKVzejJjd9lmzSXV0CLw0Id_-nO4.jpg?quality=95&as=32x13,48x19,72x29,108x43,160x64,240x96,360x144,480x192,540x216,640x256,720x288,800x320&from=bu&cs=800x320",
                        },
                        {
                            "height": 87,
                            "type": "o",
                            "width": 130,
                            "url": "https://sun9-62.userapi.com/s/v1/ig2/DIR_THon0_2NTexNFPyhTBCO5Y7ORAhoealGAxEUXZt27QJyNbdsO7WMX_NvyKVzejJjd9lmzSXV0CLw0Id_-nO4.jpg?quality=95&as=32x13,48x19,72x29,108x43,160x64,240x96,360x144,480x192,540x216,640x256,720x288,800x320&from=bu&cs=130x87",
                        },
                        {
                            "height": 133,
                            "type": "p",
                            "width": 200,
                            "url": "https://sun9-62.userapi.com/s/v1/ig2/DIR_THon0_2NTexNFPyhTBCO5Y7ORAhoealGAxEUXZt27QJyNbdsO7WMX_NvyKVzejJjd9lmzSXV0CLw0Id_-nO4.jpg?quality=95&as=32x13,48x19,72x29,108x43,160x64,240x96,360x144,480x192,540x216,640x256,720x288,800x320&from=bu&cs=200x133",
                        },
                        {
                            "height": 213,
                            "type": "q",
                            "width": 320,
                            "url": "https://sun9-62.userapi.com/s/v1/ig2/DIR_THon0_2NTexNFPyhTBCO5Y7ORAhoealGAxEUXZt27QJyNbdsO7WMX_NvyKVzejJjd9lmzSXV0CLw0Id_-nO4.jpg?quality=95&as=32x13,48x19,72x29,108x43,160x64,240x96,360x144,480x192,540x216,640x256,720x288,800x320&from=bu&cs=320x213",
                        },
                        {
                            "height": 320,
                            "type": "r",
                            "width": 510,
                            "url": "https://sun9-62.userapi.com/s/v1/ig2/DIR_THon0_2NTexNFPyhTBCO5Y7ORAhoealGAxEUXZt27QJyNbdsO7WMX_NvyKVzejJjd9lmzSXV0CLw0Id_-nO4.jpg?quality=95&as=32x13,48x19,72x29,108x43,160x64,240x96,360x144,480x192,540x216,640x256,720x288,800x320&from=bu&cs=510x320",
                        },
                    ],
                    "text": "",
                    "user_id": 100,
                    "web_view_token": "f0602dfc0ed12564f7",
                    "has_tags": False,
                    "orig_photo": {
                        "height": 320,
                        "type": "base",
                        "url": "https://sun9-62.userapi.com/s/v1/ig2/DIR_THon0_2NTexNFPyhTBCO5Y7ORAhoealGAxEUXZt27QJyNbdsO7WMX_NvyKVzejJjd9lmzSXV0CLw0Id_-nO4.jpg?quality=95&as=32x13,48x19,72x29,108x43,160x64,240x96,360x144,480x192,540x216,640x256,720x288,800x320&from=bu",
                        "width": 800,
                    },
                },
            },
            {
                "type": "link",
                "link": {
                    "url": "https://ageofmagic.game/ru-RU/",
                    "description": "Официальный портал и магазин игры Age of Magic. Бета-версия",
                    "title": "Age Of Magic - Эпическая пошаговая RPG",
                    "target": "internal",
                },
            },
        ],
        "date": 1712151736,
        "from_id": -149861500,
        "id": 159823,
        "likes": {
            "can_like": 1,
            "count": 47,
            "user_likes": 0,
            "can_publish": 1,
            "repost_disabled": False,
        },
        "owner_id": -149861500,
        "post_source": {"type": "vk"},
        "post_type": "post",
        "reposts": {"count": 5, "user_reposted": 0},
        "text": "Не забывай заглядывать в наш Магазин Подарков! Там тебя ждут не только уникальные предложения, но и ежедневные призы! \nhttps://ageofmagic.game/ru-RU/💫",
        "views": {"count": 21870},
    },
    {
        "inner_type": "wall_wallpost",
        "donut": {"is_donut": False},
        "comments": {"can_post": 0, "count": 0, "groups_can_post": True},
        "marked_as_ads": 0,
        "hash": "pNrIw5MGgel8JOYNuw",
        "type": "post",
        "push_subscription": {"is_subscribed": False},
        "attachments": [
            {
                "type": "photo",
                "photo": {
                    "album_id": -7,
                    "date": 1733842662,
                    "id": 457263102,
                    "owner_id": -149861500,
                    "access_key": "3f8de61055568660d9",
                    "post_id": 160090,
                    "sizes": [
                        {
                            "height": 51,
                            "type": "s",
                            "width": 75,
                            "url": "https://sun1-20.userapi.com/s/v1/ig2/QQJWacKg1t34BkjdT60Oftm3BAQVTgYdbfvSrEj4_3tnf0-GfJALHZOWiPaOiF-28E__UDFFEj3PGyx-nmOfM3KW.jpg?quality=95&as=32x22,48x33,72x49,108x74,160x109,240x163,360x245,480x327,540x368,640x436,720x490,1080x736,1280x872,1440x981,2208x1504&from=bu&cs=75x51",
                        },
                        {
                            "height": 89,
                            "type": "m",
                            "width": 130,
                            "url": "https://sun1-20.userapi.com/s/v1/ig2/QQJWacKg1t34BkjdT60Oftm3BAQVTgYdbfvSrEj4_3tnf0-GfJALHZOWiPaOiF-28E__UDFFEj3PGyx-nmOfM3KW.jpg?quality=95&as=32x22,48x33,72x49,108x74,160x109,240x163,360x245,480x327,540x368,640x436,720x490,1080x736,1280x872,1440x981,2208x1504&from=bu&cs=130x89",
                        },
                        {
                            "height": 411,
                            "type": "x",
                            "width": 604,
                            "url": "https://sun1-20.userapi.com/s/v1/ig2/QQJWacKg1t34BkjdT60Oftm3BAQVTgYdbfvSrEj4_3tnf0-GfJALHZOWiPaOiF-28E__UDFFEj3PGyx-nmOfM3KW.jpg?quality=95&as=32x22,48x33,72x49,108x74,160x109,240x163,360x245,480x327,540x368,640x436,720x490,1080x736,1280x872,1440x981,2208x1504&from=bu&cs=604x411",
                        },
                        {
                            "height": 550,
                            "type": "y",
                            "width": 807,
                            "url": "https://sun1-20.userapi.com/s/v1/ig2/QQJWacKg1t34BkjdT60Oftm3BAQVTgYdbfvSrEj4_3tnf0-GfJALHZOWiPaOiF-28E__UDFFEj3PGyx-nmOfM3KW.jpg?quality=95&as=32x22,48x33,72x49,108x74,160x109,240x163,360x245,480x327,540x368,640x436,720x490,1080x736,1280x872,1440x981,2208x1504&from=bu&cs=807x550",
                        },
                        {
                            "height": 872,
                            "type": "z",
                            "width": 1280,
                            "url": "https://sun1-20.userapi.com/s/v1/ig2/QQJWacKg1t34BkjdT60Oftm3BAQVTgYdbfvSrEj4_3tnf0-GfJALHZOWiPaOiF-28E__UDFFEj3PGyx-nmOfM3KW.jpg?quality=95&as=32x22,48x33,72x49,108x74,160x109,240x163,360x245,480x327,540x368,640x436,720x490,1080x736,1280x872,1440x981,2208x1504&from=bu&cs=1280x872",
                        },
                        {
                            "height": 1504,
                            "type": "w",
                            "width": 2208,
                            "url": "https://sun1-20.userapi.com/s/v1/ig2/QQJWacKg1t34BkjdT60Oftm3BAQVTgYdbfvSrEj4_3tnf0-GfJALHZOWiPaOiF-28E__UDFFEj3PGyx-nmOfM3KW.jpg?quality=95&as=32x22,48x33,72x49,108x74,160x109,240x163,360x245,480x327,540x368,640x436,720x490,1080x736,1280x872,1440x981,2208x1504&from=bu&cs=2208x1504",
                        },
                        {
                            "height": 89,
                            "type": "o",
                            "width": 130,
                            "url": "https://sun1-20.userapi.com/s/v1/ig2/QQJWacKg1t34BkjdT60Oftm3BAQVTgYdbfvSrEj4_3tnf0-GfJALHZOWiPaOiF-28E__UDFFEj3PGyx-nmOfM3KW.jpg?quality=95&as=32x22,48x33,72x49,108x74,160x109,240x163,360x245,480x327,540x368,640x436,720x490,1080x736,1280x872,1440x981,2208x1504&from=bu&cs=130x89",
                        },
                        {
                            "height": 136,
                            "type": "p",
                            "width": 200,
                            "url": "https://sun1-20.userapi.com/s/v1/ig2/QQJWacKg1t34BkjdT60Oftm3BAQVTgYdbfvSrEj4_3tnf0-GfJALHZOWiPaOiF-28E__UDFFEj3PGyx-nmOfM3KW.jpg?quality=95&as=32x22,48x33,72x49,108x74,160x109,240x163,360x245,480x327,540x368,640x436,720x490,1080x736,1280x872,1440x981,2208x1504&from=bu&cs=200x136",
                        },
                        {
                            "height": 218,
                            "type": "q",
                            "width": 320,
                            "url": "https://sun1-20.userapi.com/s/v1/ig2/QQJWacKg1t34BkjdT60Oftm3BAQVTgYdbfvSrEj4_3tnf0-GfJALHZOWiPaOiF-28E__UDFFEj3PGyx-nmOfM3KW.jpg?quality=95&as=32x22,48x33,72x49,108x74,160x109,240x163,360x245,480x327,540x368,640x436,720x490,1080x736,1280x872,1440x981,2208x1504&from=bu&cs=320x218",
                        },
                        {
                            "height": 347,
                            "type": "r",
                            "width": 510,
                            "url": "https://sun1-20.userapi.com/s/v1/ig2/QQJWacKg1t34BkjdT60Oftm3BAQVTgYdbfvSrEj4_3tnf0-GfJALHZOWiPaOiF-28E__UDFFEj3PGyx-nmOfM3KW.jpg?quality=95&as=32x22,48x33,72x49,108x74,160x109,240x163,360x245,480x327,540x368,640x436,720x490,1080x736,1280x872,1440x981,2208x1504&from=bu&cs=510x347",
                        },
                    ],
                    "text": "",
                    "user_id": 100,
                    "web_view_token": "e51019c70d150360f3",
                    "has_tags": False,
                    "orig_photo": {
                        "height": 1504,
                        "type": "base",
                        "url": "https://sun1-20.userapi.com/s/v1/ig2/QQJWacKg1t34BkjdT60Oftm3BAQVTgYdbfvSrEj4_3tnf0-GfJALHZOWiPaOiF-28E__UDFFEj3PGyx-nmOfM3KW.jpg?quality=95&as=32x22,48x33,72x49,108x74,160x109,240x163,360x245,480x327,540x368,640x436,720x490,1080x736,1280x872,1440x981,2208x1504&from=bu",
                        "width": 2208,
                    },
                },
            }
        ],
        "date": 1733842662,
        "from_id": -149861500,
        "id": 160090,
        "likes": {
            "can_like": 1,
            "count": 6,
            "user_likes": 0,
            "can_publish": 1,
            "repost_disabled": False,
        },
        "owner_id": -149861500,
        "post_source": {"type": "api"},
        "post_type": "post",
        "reposts": {"count": 0, "user_reposted": 0},
        "text": "На Аррате бушуют сильные морозы и метели. Совсем скоро начнется Время Ванов! 🥶\n\nУкройся от взора Стар'вальда, отыщи Сумрачные Талисманы и подчини Босса Северных Ванов! \n\nВыполняй магические ритуалы и вербуй Стар'вальда и других Ванов в свой отряд, пока Время Ванов не истекло! А также проходи событие \"Северные Божества\" и получи уникальную награду – аватар для профиля игрока с Ульфреном🐺\n\n#AgeofMagic #ВаныСеверныхВершин",
        "views": {"count": 580},
    },
    {
        "inner_type": "wall_wallpost",
        "donut": {"is_donut": False},
        "comments": {"can_post": 0, "count": 0, "groups_can_post": True},
        "marked_as_ads": 0,
        "hash": "aEgF1tIEtN8KiRQDeQ",
        "type": "post",
        "push_subscription": {"is_subscribed": False},
        "attachments": [
            {
                "type": "photo",
                "photo": {
                    "album_id": -7,
                    "date": 1733828263,
                    "id": 457263101,
                    "owner_id": -149861500,
                    "access_key": "8b6662fc7c38ff0683",
                    "post_id": 160088,
                    "sizes": [
                        {
                            "height": 75,
                            "type": "s",
                            "width": 63,
                            "url": "https://sun1-56.userapi.com/s/v1/ig2/L4su6A5A2GX-IhQmJar9nLlCcTwP6vH3BwO3yyyOdg07N_PsOfSUrOlwEYYmnR6rO2HLiW4eM6Ev0MtjSUBxSlMD.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu&cs=63x75",
                        },
                        {
                            "height": 130,
                            "type": "m",
                            "width": 109,
                            "url": "https://sun1-56.userapi.com/s/v1/ig2/L4su6A5A2GX-IhQmJar9nLlCcTwP6vH3BwO3yyyOdg07N_PsOfSUrOlwEYYmnR6rO2HLiW4eM6Ev0MtjSUBxSlMD.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu&cs=109x130",
                        },
                        {
                            "height": 604,
                            "type": "x",
                            "width": 506,
                            "url": "https://sun1-56.userapi.com/s/v1/ig2/L4su6A5A2GX-IhQmJar9nLlCcTwP6vH3BwO3yyyOdg07N_PsOfSUrOlwEYYmnR6rO2HLiW4eM6Ev0MtjSUBxSlMD.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu&cs=506x604",
                        },
                        {
                            "height": 688,
                            "type": "y",
                            "width": 576,
                            "url": "https://sun1-56.userapi.com/s/v1/ig2/L4su6A5A2GX-IhQmJar9nLlCcTwP6vH3BwO3yyyOdg07N_PsOfSUrOlwEYYmnR6rO2HLiW4eM6Ev0MtjSUBxSlMD.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu&cs=576x688",
                        },
                        {
                            "height": 155,
                            "type": "o",
                            "width": 130,
                            "url": "https://sun1-56.userapi.com/s/v1/ig2/L4su6A5A2GX-IhQmJar9nLlCcTwP6vH3BwO3yyyOdg07N_PsOfSUrOlwEYYmnR6rO2HLiW4eM6Ev0MtjSUBxSlMD.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu&cs=130x155",
                        },
                        {
                            "height": 239,
                            "type": "p",
                            "width": 200,
                            "url": "https://sun1-56.userapi.com/s/v1/ig2/L4su6A5A2GX-IhQmJar9nLlCcTwP6vH3BwO3yyyOdg07N_PsOfSUrOlwEYYmnR6rO2HLiW4eM6Ev0MtjSUBxSlMD.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu&cs=200x239",
                        },
                        {
                            "height": 382,
                            "type": "q",
                            "width": 320,
                            "url": "https://sun1-56.userapi.com/s/v1/ig2/L4su6A5A2GX-IhQmJar9nLlCcTwP6vH3BwO3yyyOdg07N_PsOfSUrOlwEYYmnR6rO2HLiW4eM6Ev0MtjSUBxSlMD.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu&cs=320x382",
                        },
                        {
                            "height": 609,
                            "type": "r",
                            "width": 510,
                            "url": "https://sun1-56.userapi.com/s/v1/ig2/L4su6A5A2GX-IhQmJar9nLlCcTwP6vH3BwO3yyyOdg07N_PsOfSUrOlwEYYmnR6rO2HLiW4eM6Ev0MtjSUBxSlMD.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu&cs=510x609",
                        },
                    ],
                    "text": "",
                    "user_id": 100,
                    "web_view_token": "3e07c93fa8ee840741",
                    "has_tags": False,
                    "orig_photo": {
                        "height": 688,
                        "type": "base",
                        "url": "https://sun1-56.userapi.com/s/v1/ig2/L4su6A5A2GX-IhQmJar9nLlCcTwP6vH3BwO3yyyOdg07N_PsOfSUrOlwEYYmnR6rO2HLiW4eM6Ev0MtjSUBxSlMD.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu",
                        "width": 576,
                    },
                },
            }
        ],
        "date": 1733828952,
        "from_id": -149861500,
        "id": 160089,
        "likes": {
            "can_like": 1,
            "count": 5,
            "user_likes": 0,
            "can_publish": 1,
            "repost_disabled": False,
        },
        "owner_id": -149861500,
        "post_source": {"type": "api"},
        "post_type": "post",
        "reposts": {"count": 0, "user_reposted": 0},
        "text": "Кошмарный Рейд станет ещё опаснее 🔥 Отвечаем на самые волнующие вопросы, чтобы вам было проще подготовиться к новым вызовам!\n\nВопрос: Сколько будет недоступна игра?\nОтвет: Во время технических работ игра будет недоступна около часа.\n\nВ: Какие рейды будут принудительно завершены?\nО: Во время техработ мы завершим только активные Кошмарные Рейды, все остальные рейды можно будет продолжить проходить после окончания тех. работ.\n\nВ: Сколько Камней Портала и Врат получит мой клан?\nО: Все активные кланы получат столько Камней Портала и Врат, сколько им не хватает до максимума, то есть до 36000.\n\nВ: Обновится ли Сезон Рейдов после техработ?\nО: Нет. После завершения технических работ Сезон Рейдов будет продолжен.\n\nВ: Сколько будет сложностей Кошмарного Рейда? Будут ли они все доступны после завершения техработ?\nО: Всего будет 3 сложности. Все они станут доступны, как только завершатся технические работы. Чтобы открыть первый уровень сложности, нужно пройти Кошмарный Рейд на 60%.\n\nВ: Какие награды за первое завершение сложности Кошмарного Рейда на 60%?\nО: Впервые пройдя сложности Кошмарного Рейда, ты получишь Чародейские Монеты, Ключи Познания, Серебряные Талисманы и Призмы Хаоса!\n\nВ: Будет ли новая карта в сложностях Кошмарного Рейда?\nО: Карта Кошмарного Рейда остается той же, но противники становятся сильнее с каждой новой сложностью, аналогично уже имеющимся сложностям других рейдов. Описание роста параметров противников можно увидеть в карточках сложностей.\n\nВ: Какие герои необходимы для прохождения?\nО: Тебе пригодятся все те же герои. Но не забывай, что чем сложнее рейд, тем сильнее должен быть герой. Поэтому мы рекомендуем прокачать способности до 7 уровня, а для самых сложный рейдов - пробудить их, а также усилить Медальоны.\n\nВ: Смогу ли я зайти в миссию, если у моего героя нет пробужденных способностей?\nО: Да. Пробужденные способности — лишь рекомендация. Чтобы зайти в миссию, тебе будут необходимы герои с 7 золотыми Звездами.\n\n#AgeofMagic #КошмарныйРейд #ВопросОтвет",
        "views": {"count": 837},
    },
    {
        "inner_type": "wall_wallpost",
        "donut": {"is_donut": False},
        "comments": {"can_post": 0, "count": 0, "groups_can_post": True},
        "marked_as_ads": 0,
        "hash": "yW_c6lAItA5XSoZGVw",
        "type": "post",
        "push_subscription": {"is_subscribed": False},
        "attachments": [
            {
                "type": "photo",
                "photo": {
                    "album_id": -7,
                    "date": 1733497378,
                    "id": 457263100,
                    "owner_id": -149861500,
                    "access_key": "cdd037f2622f729b48",
                    "post_id": 160086,
                    "sizes": [
                        {
                            "height": 75,
                            "type": "s",
                            "width": 63,
                            "url": "https://sun1-18.userapi.com/s/v1/ig2/s9BYQbiqYx6gsEKKmoLoSTccXqDJTUkXAVcglguK3WTjdrfR_R_7ICfqPbYDHFfaFSGrcQVZysV-QVLlRkEdC4rI.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu&cs=63x75",
                        },
                        {
                            "height": 130,
                            "type": "m",
                            "width": 109,
                            "url": "https://sun1-18.userapi.com/s/v1/ig2/s9BYQbiqYx6gsEKKmoLoSTccXqDJTUkXAVcglguK3WTjdrfR_R_7ICfqPbYDHFfaFSGrcQVZysV-QVLlRkEdC4rI.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu&cs=109x130",
                        },
                        {
                            "height": 604,
                            "type": "x",
                            "width": 506,
                            "url": "https://sun1-18.userapi.com/s/v1/ig2/s9BYQbiqYx6gsEKKmoLoSTccXqDJTUkXAVcglguK3WTjdrfR_R_7ICfqPbYDHFfaFSGrcQVZysV-QVLlRkEdC4rI.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu&cs=506x604",
                        },
                        {
                            "height": 688,
                            "type": "y",
                            "width": 576,
                            "url": "https://sun1-18.userapi.com/s/v1/ig2/s9BYQbiqYx6gsEKKmoLoSTccXqDJTUkXAVcglguK3WTjdrfR_R_7ICfqPbYDHFfaFSGrcQVZysV-QVLlRkEdC4rI.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu&cs=576x688",
                        },
                        {
                            "height": 155,
                            "type": "o",
                            "width": 130,
                            "url": "https://sun1-18.userapi.com/s/v1/ig2/s9BYQbiqYx6gsEKKmoLoSTccXqDJTUkXAVcglguK3WTjdrfR_R_7ICfqPbYDHFfaFSGrcQVZysV-QVLlRkEdC4rI.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu&cs=130x155",
                        },
                        {
                            "height": 239,
                            "type": "p",
                            "width": 200,
                            "url": "https://sun1-18.userapi.com/s/v1/ig2/s9BYQbiqYx6gsEKKmoLoSTccXqDJTUkXAVcglguK3WTjdrfR_R_7ICfqPbYDHFfaFSGrcQVZysV-QVLlRkEdC4rI.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu&cs=200x239",
                        },
                        {
                            "height": 382,
                            "type": "q",
                            "width": 320,
                            "url": "https://sun1-18.userapi.com/s/v1/ig2/s9BYQbiqYx6gsEKKmoLoSTccXqDJTUkXAVcglguK3WTjdrfR_R_7ICfqPbYDHFfaFSGrcQVZysV-QVLlRkEdC4rI.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu&cs=320x382",
                        },
                        {
                            "height": 609,
                            "type": "r",
                            "width": 510,
                            "url": "https://sun1-18.userapi.com/s/v1/ig2/s9BYQbiqYx6gsEKKmoLoSTccXqDJTUkXAVcglguK3WTjdrfR_R_7ICfqPbYDHFfaFSGrcQVZysV-QVLlRkEdC4rI.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu&cs=510x609",
                        },
                    ],
                    "text": "",
                    "user_id": 100,
                    "web_view_token": "15f0946d4990d632b4",
                    "has_tags": False,
                    "orig_photo": {
                        "height": 688,
                        "type": "base",
                        "url": "https://sun1-18.userapi.com/s/v1/ig2/s9BYQbiqYx6gsEKKmoLoSTccXqDJTUkXAVcglguK3WTjdrfR_R_7ICfqPbYDHFfaFSGrcQVZysV-QVLlRkEdC4rI.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu",
                        "width": 576,
                    },
                },
            }
        ],
        "date": 1733497825,
        "from_id": -149861500,
        "id": 160087,
        "likes": {
            "can_like": 1,
            "count": 6,
            "user_likes": 0,
            "can_publish": 1,
            "repost_disabled": False,
        },
        "owner_id": -149861500,
        "post_source": {"type": "api"},
        "post_type": "post",
        "reposts": {"count": 0, "user_reposted": 0},
        "text": "Новый вызов для тех, кто не привык сдаваться — уровни сложности Кошмарного Рейда 🥵\nПриготовься встретить еще более опасных противников, сложные эффекты миссий и, конечно же, получить ценные награды!\n\n⭐ Требования и Рекомендации:\nЧем выше сложность, тем выше требования! Чтобы участвовать в новых уровнях сложности Кошмарного Рейда, подготовь своих самых сильных героев! Тебе пригодятся герои с 6-7 Чародейскими Звездами, 7-ми или пробужденными способностями, а также Медальонами высокого уровня!\n\n🔥 Награды за прохождение:\nЧем выше сложность, тем больше и наград! За закрытие сложных Кошмарных Рейдов ты будешь получать еще больше Рейдовых Жетонов Сложности, Уникальных Жетонов, Арсенальных Жетонов XIV и Жетонов Свитков XIV!\n\n🧭 Изменения в сезоне рейдов:\nКоличество этапов рейдового сезона будет увеличено до 56! А в наградах за рейтинг сезона ты получишь Арсенальные Жетоны XIV, Жетоны Свитков XIV и вдвое больше Призм Хаоса!\n\n🛒Магазин Рейдов:\nМы убрали осколки Вильгельма из наград этапов сезона рейдов, теперь ты можешь купить их в рейдовом магазине за Рейдовые Жетоны. В магазине также появятся осколки Акеда, Марии и Астории за Рейдовые Жетоны Сложности!\n\nДля подготовки сложностей Кошмарного Рейда, 12.12 на сервере будут проведены Технические работы. Все запущенные Кошмарные Рейды будут принудительно закрыты‼Подробности будут опубликованы позже.\n\nСможет ли твой клан справиться с новыми испытаниями?\n\nГотовь отряды! Уровни сложности Кошмарных Рейдов будут доступны уже на следующей неделе! 🔥\n#AgeofMagic #КошмарныйРейд",
        "views": {"count": 1978},
    },
    {
        "inner_type": "wall_wallpost",
        "donut": {"is_donut": False},
        "comments": {"can_post": 0, "count": 0, "groups_can_post": True},
        "marked_as_ads": 0,
        "hash": "ePE35X28WqnUtFYpXQ",
        "type": "post",
        "push_subscription": {"is_subscribed": False},
        "attachments": [],
        "date": 1733492759,
        "from_id": -149861500,
        "id": 160085,
        "likes": {
            "can_like": 1,
            "count": 10,
            "user_likes": 0,
            "can_publish": 1,
            "repost_disabled": False,
        },
        "owner_id": -149861500,
        "post_source": {"type": "api"},
        "post_type": "post",
        "reposts": {"count": 0, "user_reposted": 0},
        "text": "Духи пущи, получившие физическое воплощение... Древни всегда были защитниками лесов и диких мест. Они долгое время являлись союзниками Друидов и несли свой дозор среди бескрайних просторов мира. Но Круг Друидов подвёл лес: маги не только допустили вторжение Демонов, но и устроили Катаклизм. И если Древерад смог сохранить доверие к людям, то остальные древни — нет. \n \nФлора впала в ярость и стала мстительной защитницей леса. Её колючие объятия заставят врагов медленно умирать, а стена шипов укроет союзников от внешней агрессии. Так и быть, она пощадит Друидов, которые всё ещё пытаются действовать в интересах леса. Но всех остальных чужаков ждёт неизбежная смерть. Долгая и мучительная… \n \nФлора: \n🛡провоцирует врагов на контратаки со сниженным уроном... \n🛡...возвращает врагам часть урона при атаке по союзникам \n🛡мастерица эффектов длительного урона \n🛡снимает с врагов запреты на отрицательные эффекты \n🛡умеет накладывать запреты на положительные эффекты \n🛡накладывает на союзных Друидов Щиты и Заряженные Щиты \n🛡укрывает союзных Друидов от смерти \n \n#AgeofMagic #Друиды #Защитник",
        "views": {"count": 1838},
    },
]


@pytest.mark.parametrize(
    ("last_post_id", "content_news"),
    [
        (
            0,
            [
                {
                    "id": 159823,
                    "text": "Не забывай заглядывать в наш Магазин Подарков! Там тебя ждут не только уникальные предложения, но и ежедневные призы! \nhttps://ageofmagic.game/ru-RU/💫",
                    "photos": [
                        "https://sun9-62.userapi.com/s/v1/ig2/DIR_THon0_2NTexNFPyhTBCO5Y7ORAhoealGAxEUXZt27QJyNbdsO7WMX_NvyKVzejJjd9lmzSXV0CLw0Id_-nO4.jpg?quality=95&as=32x13,48x19,72x29,108x43,160x64,240x96,360x144,480x192,540x216,640x256,720x288,800x320&from=bu&cs=800x320"
                    ],
                    "date_pub": "2024-04-03 13:42:16",
                },
                {
                    "id": 160090,
                    "text": "На Аррате бушуют сильные морозы и метели. Совсем скоро начнется Время Ванов! 🥶\n\nУкройся от взора Стар'вальда, отыщи Сумрачные Талисманы и подчини Босса Северных Ванов! \n\nВыполняй магические ритуалы и вербуй Стар'вальда и других Ванов в свой отряд, пока Время Ванов не истекло! А также проходи событие \"Северные Божества\" и получи уникальную награду – аватар для профиля игрока с Ульфреном🐺\n\n#AgeofMagic #ВаныСеверныхВершин",
                    "photos": [
                        "https://sun1-20.userapi.com/s/v1/ig2/QQJWacKg1t34BkjdT60Oftm3BAQVTgYdbfvSrEj4_3tnf0-GfJALHZOWiPaOiF-28E__UDFFEj3PGyx-nmOfM3KW.jpg?quality=95&as=32x22,48x33,72x49,108x74,160x109,240x163,360x245,480x327,540x368,640x436,720x490,1080x736,1280x872,1440x981,2208x1504&from=bu&cs=2208x1504"
                    ],
                    "date_pub": "2024-12-10 14:57:42",
                },
                {
                    "id": 160089,
                    "text": "Кошмарный Рейд станет ещё опаснее 🔥 Отвечаем на самые волнующие вопросы, чтобы вам было проще подготовиться к новым вызовам!\n\nВопрос: Сколько будет недоступна игра?\nОтвет: Во время технических работ игра будет недоступна около часа.\n\nВ: Какие рейды будут принудительно завершены?\nО: Во время техработ мы завершим только активные Кошмарные Рейды, все остальные рейды можно будет продолжить проходить после окончания тех. работ.\n\nВ: Сколько Камней Портала и Врат получит мой клан?\nО: Все активные кланы получат столько Камней Портала и Врат, сколько им не хватает до максимума, то есть до 36000.\n\nВ: Обновится ли Сезон Рейдов после техработ?\nО: Нет. После завершения технических работ Сезон Рейдов будет продолжен.\n\nВ: Сколько будет сложностей Кошмарного Рейда? Будут ли они все доступны после завершения техработ?\nО: Всего будет 3 сложности. Все они станут доступны, как только завершатся технические работы. Чтобы открыть первый уровень сложности, нужно пройти Кошмарный Рейд на 60%.\n\nВ: Какие награды за первое завершение сложности Кошмарного Рейда на 60%?\nО: Впервые пройдя сложности Кошмарного Рейда, ты получишь Чародейские Монеты, Ключи Познания, Серебряные Талисманы и Призмы Хаоса!\n\nВ: Будет ли новая карта в сложностях Кошмарного Рейда?\nО: Карта Кошмарного Рейда остается той же, но противники становятся сильнее с каждой новой сложностью, аналогично уже имеющимся сложностям других рейдов. Описание роста параметров противников можно увидеть в карточках сложностей.\n\nВ: Какие герои необходимы для прохождения?\nО: Тебе пригодятся все те же герои. Но не забывай, что чем сложнее рейд, тем сильнее должен быть герой. Поэтому мы рекомендуем прокачать способности до 7 уровня, а для самых сложный рейдов - пробудить их, а также усилить Медальоны.\n\nВ: Смогу ли я зайти в миссию, если у моего героя нет пробужденных способностей?\nО: Да. Пробужденные способности — лишь рекомендация. Чтобы зайти в миссию, тебе будут необходимы герои с 7 золотыми Звездами.\n\n#AgeofMagic #КошмарныйРейд #ВопросОтвет",
                    "photos": [
                        "https://sun1-56.userapi.com/s/v1/ig2/L4su6A5A2GX-IhQmJar9nLlCcTwP6vH3BwO3yyyOdg07N_PsOfSUrOlwEYYmnR6rO2HLiW4eM6Ev0MtjSUBxSlMD.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu&cs=576x688"
                    ],
                    "date_pub": "2024-12-10 11:09:12",
                },
                {
                    "id": 160087,
                    "text": "Новый вызов для тех, кто не привык сдаваться — уровни сложности Кошмарного Рейда 🥵\nПриготовься встретить еще более опасных противников, сложные эффекты миссий и, конечно же, получить ценные награды!\n\n⭐ Требования и Рекомендации:\nЧем выше сложность, тем выше требования! Чтобы участвовать в новых уровнях сложности Кошмарного Рейда, подготовь своих самых сильных героев! Тебе пригодятся герои с 6-7 Чародейскими Звездами, 7-ми или пробужденными способностями, а также Медальонами высокого уровня!\n\n🔥 Награды за прохождение:\nЧем выше сложность, тем больше и наград! За закрытие сложных Кошмарных Рейдов ты будешь получать еще больше Рейдовых Жетонов Сложности, Уникальных Жетонов, Арсенальных Жетонов XIV и Жетонов Свитков XIV!\n\n🧭 Изменения в сезоне рейдов:\nКоличество этапов рейдового сезона будет увеличено до 56! А в наградах за рейтинг сезона ты получишь Арсенальные Жетоны XIV, Жетоны Свитков XIV и вдвое больше Призм Хаоса!\n\n🛒Магазин Рейдов:\nМы убрали осколки Вильгельма из наград этапов сезона рейдов, теперь ты можешь купить их в рейдовом магазине за Рейдовые Жетоны. В магазине также появятся осколки Акеда, Марии и Астории за Рейдовые Жетоны Сложности!\n\nДля подготовки сложностей Кошмарного Рейда, 12.12 на сервере будут проведены Технические работы. Все запущенные Кошмарные Рейды будут принудительно закрыты‼Подробности будут опубликованы позже.\n\nСможет ли твой клан справиться с новыми испытаниями?\n\nГотовь отряды! Уровни сложности Кошмарных Рейдов будут доступны уже на следующей неделе! 🔥\n#AgeofMagic #КошмарныйРейд",
                    "photos": [
                        "https://sun1-18.userapi.com/s/v1/ig2/s9BYQbiqYx6gsEKKmoLoSTccXqDJTUkXAVcglguK3WTjdrfR_R_7ICfqPbYDHFfaFSGrcQVZysV-QVLlRkEdC4rI.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu&cs=576x688"
                    ],
                    "date_pub": "2024-12-06 15:10:25",
                },
            ],
        ),
        (
            159823,
            [
                {
                    "id": 160090,
                    "text": "На Аррате бушуют сильные морозы и метели. Совсем скоро начнется Время Ванов! 🥶\n\nУкройся от взора Стар'вальда, отыщи Сумрачные Талисманы и подчини Босса Северных Ванов! \n\nВыполняй магические ритуалы и вербуй Стар'вальда и других Ванов в свой отряд, пока Время Ванов не истекло! А также проходи событие \"Северные Божества\" и получи уникальную награду – аватар для профиля игрока с Ульфреном🐺\n\n#AgeofMagic #ВаныСеверныхВершин",
                    "photos": [
                        "https://sun1-20.userapi.com/s/v1/ig2/QQJWacKg1t34BkjdT60Oftm3BAQVTgYdbfvSrEj4_3tnf0-GfJALHZOWiPaOiF-28E__UDFFEj3PGyx-nmOfM3KW.jpg?quality=95&as=32x22,48x33,72x49,108x74,160x109,240x163,360x245,480x327,540x368,640x436,720x490,1080x736,1280x872,1440x981,2208x1504&from=bu&cs=2208x1504"
                    ],
                    "date_pub": "2024-12-10 14:57:42",
                },
                {
                    "id": 160089,
                    "text": "Кошмарный Рейд станет ещё опаснее 🔥 Отвечаем на самые волнующие вопросы, чтобы вам было проще подготовиться к новым вызовам!\n\nВопрос: Сколько будет недоступна игра?\nОтвет: Во время технических работ игра будет недоступна около часа.\n\nВ: Какие рейды будут принудительно завершены?\nО: Во время техработ мы завершим только активные Кошмарные Рейды, все остальные рейды можно будет продолжить проходить после окончания тех. работ.\n\nВ: Сколько Камней Портала и Врат получит мой клан?\nО: Все активные кланы получат столько Камней Портала и Врат, сколько им не хватает до максимума, то есть до 36000.\n\nВ: Обновится ли Сезон Рейдов после техработ?\nО: Нет. После завершения технических работ Сезон Рейдов будет продолжен.\n\nВ: Сколько будет сложностей Кошмарного Рейда? Будут ли они все доступны после завершения техработ?\nО: Всего будет 3 сложности. Все они станут доступны, как только завершатся технические работы. Чтобы открыть первый уровень сложности, нужно пройти Кошмарный Рейд на 60%.\n\nВ: Какие награды за первое завершение сложности Кошмарного Рейда на 60%?\nО: Впервые пройдя сложности Кошмарного Рейда, ты получишь Чародейские Монеты, Ключи Познания, Серебряные Талисманы и Призмы Хаоса!\n\nВ: Будет ли новая карта в сложностях Кошмарного Рейда?\nО: Карта Кошмарного Рейда остается той же, но противники становятся сильнее с каждой новой сложностью, аналогично уже имеющимся сложностям других рейдов. Описание роста параметров противников можно увидеть в карточках сложностей.\n\nВ: Какие герои необходимы для прохождения?\nО: Тебе пригодятся все те же герои. Но не забывай, что чем сложнее рейд, тем сильнее должен быть герой. Поэтому мы рекомендуем прокачать способности до 7 уровня, а для самых сложный рейдов - пробудить их, а также усилить Медальоны.\n\nВ: Смогу ли я зайти в миссию, если у моего героя нет пробужденных способностей?\nО: Да. Пробужденные способности — лишь рекомендация. Чтобы зайти в миссию, тебе будут необходимы герои с 7 золотыми Звездами.\n\n#AgeofMagic #КошмарныйРейд #ВопросОтвет",
                    "photos": [
                        "https://sun1-56.userapi.com/s/v1/ig2/L4su6A5A2GX-IhQmJar9nLlCcTwP6vH3BwO3yyyOdg07N_PsOfSUrOlwEYYmnR6rO2HLiW4eM6Ev0MtjSUBxSlMD.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu&cs=576x688"
                    ],
                    "date_pub": "2024-12-10 11:09:12",
                },
                {
                    "id": 160087,
                    "text": "Новый вызов для тех, кто не привык сдаваться — уровни сложности Кошмарного Рейда 🥵\nПриготовься встретить еще более опасных противников, сложные эффекты миссий и, конечно же, получить ценные награды!\n\n⭐ Требования и Рекомендации:\nЧем выше сложность, тем выше требования! Чтобы участвовать в новых уровнях сложности Кошмарного Рейда, подготовь своих самых сильных героев! Тебе пригодятся герои с 6-7 Чародейскими Звездами, 7-ми или пробужденными способностями, а также Медальонами высокого уровня!\n\n🔥 Награды за прохождение:\nЧем выше сложность, тем больше и наград! За закрытие сложных Кошмарных Рейдов ты будешь получать еще больше Рейдовых Жетонов Сложности, Уникальных Жетонов, Арсенальных Жетонов XIV и Жетонов Свитков XIV!\n\n🧭 Изменения в сезоне рейдов:\nКоличество этапов рейдового сезона будет увеличено до 56! А в наградах за рейтинг сезона ты получишь Арсенальные Жетоны XIV, Жетоны Свитков XIV и вдвое больше Призм Хаоса!\n\n🛒Магазин Рейдов:\nМы убрали осколки Вильгельма из наград этапов сезона рейдов, теперь ты можешь купить их в рейдовом магазине за Рейдовые Жетоны. В магазине также появятся осколки Акеда, Марии и Астории за Рейдовые Жетоны Сложности!\n\nДля подготовки сложностей Кошмарного Рейда, 12.12 на сервере будут проведены Технические работы. Все запущенные Кошмарные Рейды будут принудительно закрыты‼Подробности будут опубликованы позже.\n\nСможет ли твой клан справиться с новыми испытаниями?\n\nГотовь отряды! Уровни сложности Кошмарных Рейдов будут доступны уже на следующей неделе! 🔥\n#AgeofMagic #КошмарныйРейд",
                    "photos": [
                        "https://sun1-18.userapi.com/s/v1/ig2/s9BYQbiqYx6gsEKKmoLoSTccXqDJTUkXAVcglguK3WTjdrfR_R_7ICfqPbYDHFfaFSGrcQVZysV-QVLlRkEdC4rI.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu&cs=576x688"
                    ],
                    "date_pub": "2024-12-06 15:10:25",
                },
            ],
        ),
        (
            160087,
            [
                {
                    "id": 160090,
                    "text": "На Аррате бушуют сильные морозы и метели. Совсем скоро начнется Время Ванов! 🥶\n\nУкройся от взора Стар'вальда, отыщи Сумрачные Талисманы и подчини Босса Северных Ванов! \n\nВыполняй магические ритуалы и вербуй Стар'вальда и других Ванов в свой отряд, пока Время Ванов не истекло! А также проходи событие \"Северные Божества\" и получи уникальную награду – аватар для профиля игрока с Ульфреном🐺\n\n#AgeofMagic #ВаныСеверныхВершин",
                    "photos": [
                        "https://sun1-20.userapi.com/s/v1/ig2/QQJWacKg1t34BkjdT60Oftm3BAQVTgYdbfvSrEj4_3tnf0-GfJALHZOWiPaOiF-28E__UDFFEj3PGyx-nmOfM3KW.jpg?quality=95&as=32x22,48x33,72x49,108x74,160x109,240x163,360x245,480x327,540x368,640x436,720x490,1080x736,1280x872,1440x981,2208x1504&from=bu&cs=2208x1504"
                    ],
                    "date_pub": "2024-12-10 14:57:42",
                },
                {
                    "id": 160089,
                    "text": "Кошмарный Рейд станет ещё опаснее 🔥 Отвечаем на самые волнующие вопросы, чтобы вам было проще подготовиться к новым вызовам!\n\nВопрос: Сколько будет недоступна игра?\nОтвет: Во время технических работ игра будет недоступна около часа.\n\nВ: Какие рейды будут принудительно завершены?\nО: Во время техработ мы завершим только активные Кошмарные Рейды, все остальные рейды можно будет продолжить проходить после окончания тех. работ.\n\nВ: Сколько Камней Портала и Врат получит мой клан?\nО: Все активные кланы получат столько Камней Портала и Врат, сколько им не хватает до максимума, то есть до 36000.\n\nВ: Обновится ли Сезон Рейдов после техработ?\nО: Нет. После завершения технических работ Сезон Рейдов будет продолжен.\n\nВ: Сколько будет сложностей Кошмарного Рейда? Будут ли они все доступны после завершения техработ?\nО: Всего будет 3 сложности. Все они станут доступны, как только завершатся технические работы. Чтобы открыть первый уровень сложности, нужно пройти Кошмарный Рейд на 60%.\n\nВ: Какие награды за первое завершение сложности Кошмарного Рейда на 60%?\nО: Впервые пройдя сложности Кошмарного Рейда, ты получишь Чародейские Монеты, Ключи Познания, Серебряные Талисманы и Призмы Хаоса!\n\nВ: Будет ли новая карта в сложностях Кошмарного Рейда?\nО: Карта Кошмарного Рейда остается той же, но противники становятся сильнее с каждой новой сложностью, аналогично уже имеющимся сложностям других рейдов. Описание роста параметров противников можно увидеть в карточках сложностей.\n\nВ: Какие герои необходимы для прохождения?\nО: Тебе пригодятся все те же герои. Но не забывай, что чем сложнее рейд, тем сильнее должен быть герой. Поэтому мы рекомендуем прокачать способности до 7 уровня, а для самых сложный рейдов - пробудить их, а также усилить Медальоны.\n\nВ: Смогу ли я зайти в миссию, если у моего героя нет пробужденных способностей?\nО: Да. Пробужденные способности — лишь рекомендация. Чтобы зайти в миссию, тебе будут необходимы герои с 7 золотыми Звездами.\n\n#AgeofMagic #КошмарныйРейд #ВопросОтвет",
                    "photos": [
                        "https://sun1-56.userapi.com/s/v1/ig2/L4su6A5A2GX-IhQmJar9nLlCcTwP6vH3BwO3yyyOdg07N_PsOfSUrOlwEYYmnR6rO2HLiW4eM6Ev0MtjSUBxSlMD.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x430,480x573,540x645,576x688&from=bu&cs=576x688"
                    ],
                    "date_pub": "2024-12-10 11:09:12",
                },
            ],
        ),
        (160091, []),
    ],
)
@pytest.mark.asyncio
async def test_request(last_post_id: int, content_news: list[dict[str, Any]]):
    GameNews._get_request_news = AsyncMock(return_value=response)
    GameNews._get_last_post_id = AsyncMock(return_value=last_post_id)
    game_news = GameNews(AsyncMock())
    assert await game_news._get_content_news() == content_news
    assert GameNews._get_request_news.call_count == 1
    assert GameNews._get_last_post_id.call_count == 1
