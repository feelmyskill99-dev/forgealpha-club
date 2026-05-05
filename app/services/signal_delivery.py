import asyncio
from app.core.config import settings
from app.core.constants import Tier
from app.db.repositories.users import get_user
from app.core.logging import logger


async def send_signal_with_delay(user_id: int, text: str, min_tier: int):
    """Отправляет сигнал с задержкой в зависимости от tier пользователя."""
    user = await get_user(user_id)
    if not user:
        return

    user_tier = user["tier"]
    if user_tier < min_tier:
        return

    delay = settings.TIER_DELAYS.get(user_tier, 60)
    if delay > 0:
        await asyncio.sleep(delay)

    # Здесь будет реальная отправка через бота
    logger.info("Signal sent", user_id=user_id, tier=user_tier, delay=delay, text=text[:50])