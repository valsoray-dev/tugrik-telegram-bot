"""Keyboards"""

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)

from constants import buttons

# Reply Keyboard
forever_keyboard = (
    ReplyKeyboardMarkup(resize_keyboard=True)
    .add(buttons.CURRENT_CURRENCY_TEXT)
    .add(buttons.STATS_COMMAND_TEXT)
    .add(buttons.STOP_COMMAND_TEXT)
)

forever_keyboard_register = (
    ReplyKeyboardMarkup(resize_keyboard=True)
    .add(buttons.CURRENT_CURRENCY_TEXT)
    .add(buttons.START_COMMAND_TEXT)
)


# Inline Keyboard
now_button = InlineKeyboardButton(
    text="Ресурс",
    url="https://www.xe.com/currencyconverter/convert/?Amount=1&From=UAH&To=MNT",
)
now_inline = InlineKeyboardMarkup().add(now_button)
