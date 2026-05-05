import pytest

from app.db.repositories.payments import get_payment
from app.services.payments import confirm_payment_and_activate, create_invoice
from app.services.subscriptions import get_user_tier, is_subscription_active


@pytest.mark.asyncio
async def test_create_invoice() -> None:
    payment_id = await create_invoice(123456, 1, 100.0)
    assert payment_id > 0

    payment = await get_payment(payment_id)
    assert payment is not None
    assert payment["status"] == "pending"


@pytest.mark.asyncio
async def test_confirm_payment_activates_subscription() -> None:
    user_id = 123456
    payment_id = await create_invoice(user_id, 2, 149.0)

    confirmed = await confirm_payment_and_activate(payment_id, tx_hash="test_tx")

    assert confirmed is True
    assert await get_user_tier(user_id) == 2
    assert await is_subscription_active(user_id) is True
