"""A small telegram bot that sends the exchange rate MNT - UAH every day at 5:00 UTC."""

import asyncio

from aiogram import Dispatcher, executor
from loguru import logger

import handlers
from loader import bot, dp, users
from utils import scheduler
from utils.functions import send_currency_schedule
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher: Dispatcher):
    """When bot started"""

    await set_default_commands(dispatcher)
    task = scheduler.start(function=send_currency_schedule, bot=bot, users=users)
    asyncio.create_task(task)
    logger.info("All is ready! The bot is running.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
