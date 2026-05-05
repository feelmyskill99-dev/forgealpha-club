from datetime import datetime, timedelta

from app.db.repositories.users import get_user, update_user_tier


async def activate_subscription(user_id: int, tier: int, months: int = 1) -> None:
    subscribed_until = (datetime.now() + timedelta(days=30 * months)).isoformat()
    await update_user_tier(
        user_id=user_id,
        tier=tier,
        subscribed_until=subscribed_until,
    )


async def get_user_tier(user_id: int) -> int:
    user = await get_user(user_id)
    if user is None:
        return 0

    return int(user.get("tier", 0))


async def is_subscription_active(user_id: int) -> bool:
    user = await get_user(user_id)
    if user is None:
        return False

    status = user.get("subscription_status")
    subscribed_until = user.get("subscribed_until")

    if status != "active" or subscribed_until is None:
        return False

    return datetime.fromisoformat(str(subscribed_until)) > datetime.now()