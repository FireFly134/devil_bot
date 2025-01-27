"""Напоминалка по подпискам"""
import logging
from datetime import datetime

from aiogram.enums import ParseMode

from services.reminder.clear_rock import clear_rock
from services.reminder.reminder_energy import reminder_energy
from services.reminder.reminder_kz import reminder_kz
from services.reminder.reminder_zero import reminder_zero




if __name__ == "__main__":
    time = datetime.now()  # текущее время
    ### Проверка на наличия энергии по времени для подписчиков ###
    if int(time.strftime("%M")) == 0:
        reminder_energy()
        if int(time.strftime("%H")) == 14:
            reminder_zero()
        if int(time.strftime("%H")) == 15:
            clear_rock()

    if int(time.strftime("%M")) == 30:
        reminder_kz()

