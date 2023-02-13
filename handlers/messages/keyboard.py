"""Handler for keyboards"""

from aiogram import types

from constants import buttons
from handlers.commands import default
from loader import dp


@dp.message_handler(lambda msg: msg.text in buttons.BUTTON_TEXTS_LIST)
async def keyboard_handler(message: types.Message):
    """Handler for keyboards"""

    # TODO: сделать КРАСИВО (rework)
    text = message.text
    match text:
        case buttons.CURRENT_CURRENCY_TEXT:
            await default.now_command(message)
        case buttons.STOP_COMMAND_TEXT:
            await default.stop_command(message)
        case buttons.STATS_COMMAND_TEXT:
            await default.stats_command(message)
        case buttons.START_COMMAND_TEXT:
            await default.start_command(message)
