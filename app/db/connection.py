import aiosqlite
from app.core.config import settings
from app.core.logging import logger


async def get_db():
    db = await aiosqlite.connect(settings.DATABASE_URL.replace("sqlite+aiosqlite:///", ""))
    db.row_factory = aiosqlite.Row
    return db


async def init_db():
    async with aiosqlite.connect(settings.DATABASE_URL.replace("sqlite+aiosqlite:///", "")) as db:
        # Run migrations
        with open("app/db/migrations/001_init.sql", "r", encoding="utf-8") as f:
            await db.executescript(f.read())
        await db.commit()
        logger.info("Database initialized")