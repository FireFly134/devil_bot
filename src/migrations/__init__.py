"""SQL Alchemy metadata. Used for all models and migrations"""
from gino import Gino

from config import DB_URI
import logging

logging.basicConfig()
logging.getLogger('gino.engine._SAEngine').setLevel(logging.ERROR)

db = Gino(DB_URI)

METADATA = db
