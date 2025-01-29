"""Напоминалка по подпискам"""
from datetime import datetime

from services.reminder.reminder_and_cleaner_rock import (
    clear_rock,
    reminder_zero,
)
from services.reminder.reminder_energy import reminder_energy
from services.reminder.reminder_kz import reminder_kz

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
