from app.core.logging import logger
from app.db.repositories.payments import confirm_payment, create_payment, get_payment
from app.db.repositories.users import create_or_update_user
from app.services.subscriptions import activate_subscription


async def create_invoice(user_id: int, tier: int, amount: float) -> int:
    """Create a pending payment invoice. Does not upgrade the user."""
    payment_id = await create_payment(user_id, tier, amount)
    logger.info("payment_invoice_created", payment_id=payment_id, user_id=user_id, tier=tier)
    return payment_id


async def confirm_invoice(
    payment_id: int,
    user_id: int,
    tier: int,
    tx_hash: str | None = None,
) -> None:
    """Confirm payment and only then activate subscription."""
    await create_or_update_user(user_id=user_id, username=None)
    await confirm_payment(payment_id, tx_hash=tx_hash)
    await activate_subscription(user_id=user_id, tier=tier)
    logger.info("payment_confirmed", payment_id=payment_id, user_id=user_id, tier=tier)


async def confirm_payment_and_activate(payment_id: int, tx_hash: str | None = None) -> bool:
    """Confirm an existing pending payment using its stored user and tier."""
    payment = await get_payment(payment_id)
    if payment is None:
        return False

    await confirm_invoice(
        payment_id=payment_id,
        user_id=int(payment["user_id"]),
        tier=int(payment["tier"]),
        tx_hash=tx_hash,
    )
    return True
