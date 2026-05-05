from app.db.connection import get_db
from app.core.constants import Tier


async def get_user(user_id: int):
    async with await get_db() as db:
        cursor = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None


async def create_user(user_id: int, username: str | None = None, referred_by: int | None = None):
    async with await get_db() as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username, referred_by) VALUES (?, ?, ?)",
            (user_id, username, referred_by)
        )
        await db.commit()


async def update_user_tier(user_id: int, new_tier: int, months: int = 1):
    from datetime import datetime, timedelta
    until = (datetime.now() + timedelta(days=30 * months)).isoformat()
    async with await get_db() as db:
        await db.execute(
            "UPDATE users SET tier = ?, subscribed_until = ? WHERE user_id = ?",
            (new_tier, until, user_id)
        )
        await db.commit()