from typing import Any

from app.core.constants import PaymentStatus
from app.db.connection import get_db


async def create_payment(
    user_id: int,
    tier: int,
    amount: float,
    tx_hash: str | None = None,
) -> int:
    async with get_db() as db:
        cursor = await db.execute(
            """
            INSERT INTO payments (user_id, tier, amount, tx_hash, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, tier, amount, tx_hash, PaymentStatus.PENDING.value),
        )
        await db.commit()
        payment_id = cursor.lastrowid
        if payment_id is None:
            raise RuntimeError("Failed to create payment")
        return int(payment_id)


async def get_payment(payment_id: int) -> dict[str, Any] | None:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM payments WHERE id = ?", (payment_id,))
        row = await cursor.fetchone()
        return None if row is None else dict(row)


async def get_pending_payments(limit: int = 50) -> list[dict[str, Any]]:
    async with get_db() as db:
        cursor = await db.execute(
            """
            SELECT *
            FROM payments
            WHERE status = ?
            ORDER BY created_at ASC
            LIMIT ?
            """,
            (PaymentStatus.PENDING.value, limit),
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def confirm_payment(payment_id: int, tx_hash: str | None = None) -> None:
    async with get_db() as db:
        await db.execute(
            """
            UPDATE payments
            SET
                status = ?,
                tx_hash = COALESCE(?, tx_hash),
                confirmed_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (PaymentStatus.CONFIRMED.value, tx_hash, payment_id),
        )
        await db.commit()
