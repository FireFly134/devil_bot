"""Module for migrations.
Used to track changes in db schema automatically.
Extend if new modules with models added."""
from .events import Events
from .clans import Clans
from .heroes_of_users import HeroesOfUsers
from .post_news import PostNews
from .telegram_users import User
from .text_table import TextTable
