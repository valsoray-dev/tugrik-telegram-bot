"""Scheduler"""

from typing import Callable

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger
from pytz import utc


async def start(*args, function: Callable, hour: int = 5, **kwargs) -> None:
    """Execute a `function` every day at a specific `hour`.

    Args:
        function (Callable): function to execute
        hour (int, optional): defaults to 5.
    """

    scheduler = AsyncIOScheduler()
    trigger = CronTrigger(hour=hour, timezone=utc)

    scheduler.add_job(function, trigger, args, kwargs)
    scheduler.start()

    logger.debug(
        "Scheduler installed. [{0}] will be executing every day at [{1}:00] UTC.",
        function.__name__,
        hour,
    )
