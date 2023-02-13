"""The default commands that are specified in the bot commands"""

from datetime import datetime, timezone

from aiogram import types

from classes.user import User
from constants import buttons
from keyboards import keyboard
from loader import dp, users
from utils import functions


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    """Start command function"""

    user: User = {"user_id": message.from_user.id}
    if not await users.find_one(user):
        await message.reply(
            "Теперь я буду отправлять вам курс монгольского тугрика к гривне каждый день в 5:00 UTC",
            reply_markup=keyboard.forever_keyboard,
        )

        user["username"] = message.from_user.username
        user["reg_date"] = datetime.isoformat(datetime.now(timezone.utc))
        user["schedules"] = 0

        await users.insert_one(user)
    else:
        await message.reply(
            "Вы уже зарегистрированы на рассылку. Курс приходит каждый день в 5:00 UTC",
            reply_markup=keyboard.forever_keyboard,
        )


@dp.message_handler(commands=["stop"])
async def stop_command(message: types.Message):
    """Stop command function"""

    user: User = {"user_id": message.from_user.id}
    if await users.find_one(user):
        await users.delete_one(user)
        await message.reply(
            "Вы были удалены из рассылки.",
            reply_markup=keyboard.forever_keyboard_register,
        )
    else:
        await message.reply(
            "Вы не зарегистрированы! Введите команду /start или "
            f"нажмите на кнопку <code>{buttons.START_COMMAND_TEXT}</code>"
        )


@dp.message_handler(commands=["now"])
@dp.throttled(rate=5)
async def now_command(message: types.Message):
    """Now command function"""

    currency = await functions.get_currency()
    text = await functions.get_currency_string(currency)
    await message.reply(
        text, disable_web_page_preview=True, reply_markup=keyboard.now_inline
    )


@dp.message_handler(commands=["stats"])
async def stats_command(message: types.Message):
    """Stats command function"""

    user: User = {"user_id": message.from_user.id}
    if user := await users.find_one(user):
        statistics = await functions.get_stats_string(user)
        await message.reply(statistics)
    else:
        await message.reply(
            "Вы не зарегистрированы! Введите команду /start или "
            f"нажмите на кнопку <code>{buttons.START_COMMAND_TEXT}</code>"
        )
