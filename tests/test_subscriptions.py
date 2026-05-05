import pytest
from app.services.subscriptions import is_subscription_active, get_user_tier


@pytest.mark.asyncio
async def test_get_user_tier():
    tier = await get_user_tier(123456)
    assert tier >= 0