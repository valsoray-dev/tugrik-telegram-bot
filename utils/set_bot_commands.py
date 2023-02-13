"""Set default commands for bot"""

from aiogram import Dispatcher, types


async def set_default_commands(dp: Dispatcher):
    """Set default commands for bot"""

    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Подписаться на рассылку"),
            types.BotCommand("now", "Получить текущий курс"),
            types.BotCommand("stats", "Статистика"),
            types.BotCommand("stop", "Отписаться от рассылки"),
        ]
    )
