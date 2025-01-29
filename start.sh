#!/usr/bin/env bash
# проверка миграций
alembic -c alembic.ini upgrade head

# загрузка переводов
echo "Запускаю бота"
python3 src/main.py
