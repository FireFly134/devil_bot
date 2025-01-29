"""Файл для инициализации состояний."""
from aiogram import Router
from aiogram.fsm.state import State, StatesGroup

form_router = Router()


class Regisration(StatesGroup):
    """Состояние регистрации."""

    name = State()
    user_id = State()
    hero_id = State()


class UpdateTimeChangeClanTask(StatesGroup):
    """Состояние обновления времени для клана."""

    hour = State()
    chat_id = State()


class SettingProfile(StatesGroup):
    """Состояние для настроек профиля."""

    is_active = State()
    edit_name = State()
    time_zone = State()
    is_tz = State()
    level = State()
    hero_user_id = State()
    hero_id = State()
    name = State()
