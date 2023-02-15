"""Errors handler"""

from aiogram import exceptions, types
from loguru import logger

from data import config
from loader import bot, dp


@dp.errors_handler()
async def error_handler(update: types.Update, error: BaseException):
    """Error handler"""

    match error:
        case exceptions.BotBlocked:
            logger.log("User [@%s] has blocked bot.", update.message.from_user.username)
            return True
        case _:
            logger.exception(error)
            await bot.send_message(
                config.ADMIN_ID,
                f"<b>Произошла непредвиденная ошибка!</b>\n\n<code>{error.__class__.__name__}: {error}</code>",
            )
            await bot.send_message(
                update.message.from_id,
                "<b>Что-то пошло не так...</b>\nДанные об ошибке были отпралены разработчику",
            )
            return True
