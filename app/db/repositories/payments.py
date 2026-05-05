from app.db.connection import get_db
from app.core.constants import PaymentStatus


async def create_payment(user_id: int, tier: int, amount: float, tx_hash: str | None = None):
    async with await get_db() as db:
        await db.execute(
            """INSERT INTO payments (user_id, tier, amount, tx_hash, status)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, tier, amount, tx_hash, PaymentStatus.PENDING)
        )
        await db.commit()
        cursor = await db.execute("SELECT last_insert_rowid()")
        return (await cursor.fetchone())[0]


async def confirm_payment(payment_id: int):
    from datetime import datetime
    async with await get_db() as db:
        await db.execute(
            "UPDATE payments SET status = ?, confirmed_at = ? WHERE id = ?",
            (PaymentStatus.CONFIRMED, datetime.now().isoformat(), payment_id)
        )
        await db.commit()


async def get_pending_payments():
    async with await get_db() as db:
        cursor = await db.execute("SELECT * FROM payments WHERE status = ?", (PaymentStatus.PENDING,))
        return [dict(row) for row in await cursor.fetchall()]