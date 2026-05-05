from typing import Any

from app.db.connection import get_db


async def add_signal(
    title: str,
    description: str,
    source: str | None = None,
    min_tier: int = 0,
) -> int:
    async with get_db() as db:
        cursor = await db.execute(
            """
            INSERT INTO signals (title, description, source, min_tier)
            VALUES (?, ?, ?, ?)
            """,
            (title, description, source, min_tier),
        )
        await db.commit()
        signal_id = cursor.lastrowid
        if signal_id is None:
            raise RuntimeError("Failed to create signal")
        return int(signal_id)


async def get_recent_signals(limit: int = 5) -> list[dict[str, Any]]:
    async with get_db() as db:
        cursor = await db.execute(
            """
            SELECT *
            FROM signals
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,),
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
