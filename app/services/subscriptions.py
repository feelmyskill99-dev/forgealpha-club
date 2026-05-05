from datetime import datetime, timedelta
from app.db.repositories.users import get_user, update_user_tier
from app.core.constants import Tier


async def activate_subscription(user_id: int, tier: int, months: int = 1):
    """Активирует подписку только после подтверждённой оплаты."""
    until = (datetime.now() + timedelta(days=30 * months)).isoformat()
    await update_user_tier(user_id, tier)
    # Здесь можно добавить запись в историю подписок


async def is_subscription_active(user_id: int) -> bool:
    user = await get_user(user_id)
    if not user:
        return False
    if user.get("banned_until"):
        return False
    if user.get("subscribed_until"):
        return datetime.fromisoformat(user["subscribed_until"]) > datetime.now()
    return user["tier"] > 0


async def get_user_tier(user_id: int) -> int:
    user = await get_user(user_id)
    return user["tier"] if user else 0