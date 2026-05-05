from app.core.logging import logger


async def check_pending_payments() -> None:
    """
    Placeholder for real payment verification.

    Real implementation should:
    - load pending payments from database;
    - verify transaction hash against payment provider / blockchain;
    - confirm payment only after successful verification;
    - activate subscription after confirmed payment.
    """
    logger.info("payment_checker_started")
    logger.info("payment_checker_finished", checked=0)