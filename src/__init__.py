from aiogram import Router
from aiogram.fsm.state import State, StatesGroup

form_router = Router()

class Regisration(StatesGroup):
    name = State()
    user_id = State()
    hero_id = State()