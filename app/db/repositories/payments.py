from typing import Any

from app.db.connection import get_db
from app.core.constants import PaymentStatus


async def create_payment(
    user_id: int,
    tier: int,
    amount: float,
    tx_hash: str | None = None,
) -> int:
    async with get_db() as db:
        cursor = await db.execute(
            """
            INSERT INTO payments (
                user_id,
                tier,
                amount,
                tx_hash,
                status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                tier,
                amount,
                tx_hash,
                PaymentStatus.PENDING.value,
            ),
        )
        await db.commit()

        payment_id = cursor.lastrowid
        if payment_id is None:
            raise RuntimeError("Failed to create payment")

        return int(payment_id)


async def get_payment(payment_id: int) -> dict[str, Any] | None:
    async with get_db() as db:
        cursor = await db.execute(
            """
            SELECT *
            FROM payments
            WHERE id = ?
            """,
            (payment_id,),
        )
        row = await cursor.fetchone()

        if row is None:
            return None

        return dict(row)


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
            (
                PaymentStatus.CONFIRMED.value,
                tx_hash,
                payment_id,
            ),
        )
        await db.commit()