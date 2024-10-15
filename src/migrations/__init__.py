"""SQL Alchemy metadata. Used for all models and migrations"""
import asyncio
from gino import Gino

from config import DB_URI
import logging

logging.basicConfig()
logging.getLogger('gino.engine._SAEngine').setLevel(logging.ERROR)

db = Gino()

async def main():
    await db.set_bind(DB_URI)

asyncio.get_event_loop().run_until_complete(main())
METADATA = db
