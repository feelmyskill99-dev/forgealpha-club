from typing import Any

from app.db.connection import get_db


async def create_or_update_user(user_id: int, username: str | None) -> None:
    async with get_db() as db:
        await db.execute(
            """
            INSERT INTO users (user_id, username)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                updated_at = CURRENT_TIMESTAMP
            """,
            (user_id, username),
        )
        await db.commit()


async def get_user(user_id: int) -> dict[str, Any] | None:
    async with get_db() as db:
        cursor = await db.execute(
            """
            SELECT *
            FROM users
            WHERE user_id = ?
            """,
            (user_id,),
        )
        row = await cursor.fetchone()
        return None if row is None else dict(row)


async def update_user_tier(
    user_id: int,
    tier: int,
    subscribed_until: str | None = None,
) -> None:
    async with get_db() as db:
        if subscribed_until is None:
            await db.execute(
                """
                UPDATE users
                SET tier = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
                """,
                (tier, user_id),
            )
        else:
            await db.execute(
                """
                UPDATE users
                SET
                    tier = ?,
                    subscription_status = 'active',
                    subscribed_until = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
                """,
                (tier, subscribed_until, user_id),
            )
        await db.commit()
