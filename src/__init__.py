from aiogram import Router
from aiogram.fsm.state import State, StatesGroup

form_router = Router()


class Regisration(StatesGroup):
    name = State()
    user_id = State()
    hero_id = State()


class UpdateTimeChangeClanTask(StatesGroup):
    hour = State()
    chat_id = State()


class SettingProfile(StatesGroup):
    is_active = State()
    edit_name = State()
    time_zone = State()
    is_tz = State()
    level = State()
    user_id = State()
    hero_id = State()
