"""Functions"""
import os
import re
from base64 import b64encode
from datetime import datetime, timezone

import aiohttp
from aiogram import Bot
from loguru import logger
from pymongo.collection import Collection

from keyboards import keyboard


async def get_xe_key() -> None:
    """..."""

    base_url = "https://www.xe.com"
    app_js_regex = r"\/_next\/static\/chunks\/pages\/_app-.{23}"
    key_regex = r"lodestar.{15}(.{32})"

    async with aiohttp.ClientSession() as session:

        async with session.get(base_url) as xe_site:
            xe_site_body = str(await xe_site.read())
            app_js_refer = re.findall(app_js_regex, xe_site_body)[0]

        async with session.get(base_url + app_js_refer) as app_js:
            app_js_body = str(await app_js.read())
            key = re.findall(key_regex, app_js_body)[0]

    os.environ["XE_KEY"] = f"lodestar:{key}"
    logger.debug(
        "The key for authorization on the site is saved as environment variable."
    )


async def get_currency() -> float:
    """Get currency UAH -> MNT

    Returns:
        currency (float): `1` UAH -> `currency` MNT
    """

    auth = b64encode(bytes(os.getenv("XE_KEY"), encoding="utf-8"))
    headers = {"Authorization": f"Basic {str(auth)[2:-1]}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://www.xe.com/api/protected/midmarket-converter/", headers=headers
        ) as request:
            json: dict = await request.json()
            mnt: float = json["rates"]["MNT"]
            uah: float = json["rates"]["UAH"]

    return mnt / uah


async def get_currency_string(currency: float) -> str:
    """Get formatted currency text to send

    Args:
        currency (float): `1` UAH -> `currency` MNT

    Returns:
        text (str): formatted text
    """

    date = datetime.now(timezone.utc).strftime("%d/%m/%Y, %H:%M:%S")
    currency = round(currency, 2)

    return (
        f"На момент <code>{date} UTC</code> курс составляет "
        f"<code>1</code> Украинская гривна 🇺🇦 = <code>{currency}</code> Монгольских тугриков 🇲🇳\n"
    )


async def get_quote() -> dict:
    """Get quote from forismatic.com

    Returns:
        dict: json quote
    """

    data = {"method": "getQuote", "format": "json", "lang": "ru"}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://api.forismatic.com/api/1.0/", data=data
        ) as request:
            return await request.json()


async def get_quote_string(quote_json: dict) -> str:
    """Get formatted quote text to send

    Args:
        quote_json (dict): quote json table

    Returns:
        quote: formatted text
    """

    return (
        f'<b>“{quote_json["quoteText"]}”</b>\n\n'
        f'<i>— {quote_json["quoteAuthor"] or "Неизвестный"}</i>'
    )


async def get_stats_string(user: dict) -> str:
    """Get formatted stats text to send

    Args:
        user (dict): user from DB

    Returns:
        str: formatted string
    """

    reg_date = datetime.fromisoformat(user["reg_date"])
    return (
        f"• Никнейм: @{user['username']}\n"
        f"• ИД в базе данных: <code>{user['db_id']}</code>\n"
        f"• Дата регистрации: <code>{reg_date.strftime('%d/%m/%Y, %H:%M:%S')} UTC</code>\n"
        f"• Количество отправленных сообщений: <code>[{user['schedules']}]</code>"
    )


async def send_currency_schedule(bot: Bot, users: Collection):
    """A function that sends a quote & currency to all users from collection

    Args:
        bot (Bot): Bot class
        users (Collection): Users collection
    """

    currency = await get_currency()
    quote = await get_quote()

    currency_string = await get_currency_string(currency)
    quote_string = await get_quote_string(quote)

    async for user in users.find():
        await bot.send_message(user["user_id"], quote_string)
        await bot.send_message(
            chat_id=user["user_id"],
            text=currency_string,
            disable_web_page_preview=True,
            reply_markup=keyboard.now_inline,
        )
        await users.update_one({"user_id": user["user_id"]}, {"$inc": {"schedules": 1}})
