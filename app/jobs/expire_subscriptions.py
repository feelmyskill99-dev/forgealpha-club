from app.db.connection import get_db


async def expire_subscriptions() -> None:
    async with get_db() as db:
        await db.execute(
            """
            UPDATE users
            SET
                tier = 0,
                subscription_status = 'expired',
                updated_at = CURRENT_TIMESTAMP
            WHERE
                subscription_status = 'active'
                AND subscribed_until IS NOT NULL
                AND subscribed_until < CURRENT_TIMESTAMP
            """
        )
        await db.commit()
