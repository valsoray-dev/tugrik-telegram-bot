"""Errors handler"""

import traceback

from aiogram import exceptions, types
from loguru import logger

from data import config
from loader import bot, dp


@dp.errors_handler()
async def error_handler(update: types.Update, error: Exception):
    """Error handler"""

    match error:
        case exceptions.BotBlocked:
            logger.log("User [@%s] has blocked bot.", update.message.from_user.username)
            return True
        case _:
            exception = traceback.format_exc()
            logger.error(exception)
            await bot.send_message(
                config.ADMIN_ID,
                f"<b>Произошла непредвиденная ошибка!</b>\n\nКод ошибки:\n<code>{exception}</code>",
            )
            await bot.send_message(
                update.message.from_id,
                "<b>Что-то пошло не так...</b>\nДанные об ошибке были отпралены разработчику",
            )
            return True
