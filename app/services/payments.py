from app.core.logging import logger
from app.db.repositories.payments import confirm_payment, create_payment
from app.db.repositories.users import update_user_tier


async def create_invoice(user_id: int, tier: int, amount: float) -> int:
    """Create a pending payment invoice. Does not upgrade the user."""
    payment_id = await create_payment(user_id, tier, amount)
    logger.info("payment_invoice_created", payment_id=payment_id, user_id=user_id, tier=tier)
    return payment_id


async def confirm_invoice(payment_id: int, user_id: int, tier: int, tx_hash: str | None = None) -> None:
    """Confirm payment and only then upgrade user tier."""
    await confirm_payment(payment_id, tx_hash=tx_hash)
    await update_user_tier(user_id, tier)
    logger.info("payment_confirmed", payment_id=payment_id, user_id=user_id, tier=tier)