from app.db.connection import get_db


async def create_signal(text: str, min_tier: int, source: str = "onchain"):
    async with await get_db() as db:
        await db.execute(
            "INSERT INTO signals (text, min_tier, source) VALUES (?, ?, ?)",
            (text, min_tier, source)
        )
        await db.commit()
        cursor = await db.execute("SELECT last_insert_rowid()")
        return (await cursor.fetchone())[0]


async def get_recent_signals(limit: int = 5):
    async with await get_db() as db:
        cursor = await db.execute(
            "SELECT * FROM signals ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )
        return [dict(row) for row in await cursor.fetchall()]