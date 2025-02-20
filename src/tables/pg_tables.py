"""Module for migrations.
Used to track changes in db schema automatically.
Extend if new modules with models added."""
from src.tables.clans import Clans
from src.tables.events import Events
from src.tables.heroes_of_users import HeroesOfUsers
from src.tables.post_news import PostNews
from src.tables.telegram_users import User
from src.tables.text_table import TextTable
