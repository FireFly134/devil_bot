"""SQL Alchemy metadata. Used for all models and migrations"""
import asyncio
from gino import Gino

from config import settings
import logging

logging.basicConfig()
logging.getLogger('gino.engine._SAEngine').setLevel(logging.ERROR)

db = Gino()

METADATA = db

async def run_connection_db():
    await db.set_bind(settings.DB_URI)

# if not db.is_bound():
#     asyncio.get_event_loop().run_until_complete(main())