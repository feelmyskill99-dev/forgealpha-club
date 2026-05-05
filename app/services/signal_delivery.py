import asyncio
from typing import Any

from aiogram import Bot

from app.core.config import settings
from app.core.logging import logger
from app.db.repositories.users import get_user


async def send_signal_with_delay(
    bot: Bot,
    user_id: int,
    signal: dict[str, Any],
) -> None:
    user = await get_user(user_id)
    tier = int(user.get("tier", 0)) if user else 0
    delay = settings.TIER_DELAYS.get(tier, 0)

    if delay > 0:
        await asyncio.sleep(delay)

    await bot.send_message(
        chat_id=user_id,
        text=f"📡 {signal['title']}\n\n{signal['description']}",
    )

    logger.info("signal_sent", user_id=user_id, tier=tier, delay=delay)