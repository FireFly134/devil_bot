"""SQL Alchemy metadata. Used for all models and migrations"""
from gino import Gino

from config import settings
import logging

logging.basicConfig()
logging.getLogger('gino.engine._SAEngine').setLevel(logging.ERROR)

db = Gino()
metadata = db

async def run_connection_db():
    await db.set_bind(settings.DB_URI)
