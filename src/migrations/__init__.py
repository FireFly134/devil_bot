"""SQL Alchemy metadata. Used for all models and migrations"""
from gino.ext.starlette import Gino

from config import settings
import logging

logging.basicConfig()
logging.getLogger('gino.engine._SAEngine').setLevel(logging.ERROR)

db = Gino(dsn=settings.DB_URI, use_connection_for_request=True)
METADATA = db

async def run_connection_db():
    await db.set_bind(settings.DB_URI)
