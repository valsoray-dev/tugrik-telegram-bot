"""Commands for admins only"""

import os

from aiogram import types

from data import config
from loader import bot, dp, users
from utils.functions import send_currency_schedule


def is_admin(msg: types.Message) -> bool:
    """Check if user is admin"""

    return msg.from_user.id == config.ADMIN_ID


@dp.message_handler(is_admin, commands=["send_schedule"])
async def send_schedule_command(message: types.Message):
    """Send schedule command function"""

    await send_currency_schedule(bot=bot, users=users)


@dp.message_handler(is_admin, commands=["raise"])
async def raise_error(message: types.Message):
    """..."""
    raise Exception("TEST")
