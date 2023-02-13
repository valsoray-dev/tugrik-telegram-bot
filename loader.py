"""Loader for bot"""

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection
from pymongo.database import Database

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

client = AsyncIOMotorClient(config.MONGODB_STRING)
db: Database = client.users
users: Collection = db.users_list

logger.add("logs/logs.log", format="[{time}] [{level}]: {message}", rotation="1 day")
