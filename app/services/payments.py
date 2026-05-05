from datetime import datetime
from app.db.repositories.payments import create_payment, confirm_payment
from app.db.repositories.users import update_user_tier
from app.core.constants import PaymentStatus, Tier
from app.core.logging import logger


async def create_invoice(user_id: int, tier: int, amount: float) -> int:
    """Создаёт платёж в статусе pending. НЕ апгрейдит пользователя сразу!"""
    payment_id = await create_payment(user_id, tier, amount)
    logger.info("Payment created", payment_id=payment_id, user_id=user_id, tier=tier, status=PaymentStatus.PENDING)
    return payment_id


async def confirm_payment_and_activate(user_id: int, payment_id: int, tier: int):
    """Подтверждает платёж и только потом активирует подписку."""
    await confirm_payment(payment_id)
    await update_user_tier(user_id, tier)
    logger.info("Payment confirmed and subscription activated", payment_id=payment_id, user_id=user_id, tier=tier)


async def get_payment_status(payment_id: int) -> str:
    # В реальной версии — запрос к БД
    return PaymentStatus.PENDING  # заглушка для демо