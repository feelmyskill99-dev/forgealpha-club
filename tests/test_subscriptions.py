import pytest

from app.db.repositories.users import create_or_update_user
from app.services.subscriptions import activate_subscription, get_user_tier, is_subscription_active


@pytest.mark.asyncio
async def test_get_user_tier_for_unknown_user() -> None:
    tier = await get_user_tier(123456)
    assert tier == 0


@pytest.mark.asyncio
async def test_activate_subscription() -> None:
    user_id = 222
    await create_or_update_user(user_id, "tester")
    await activate_subscription(user_id=user_id, tier=1)

    assert await get_user_tier(user_id) == 1
    assert await is_subscription_active(user_id) is True
