from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import aiosqlite

from app.core.config import settings


@asynccontextmanager
async def get_db() -> AsyncIterator[aiosqlite.Connection]:
    db = await aiosqlite.connect(settings.DATABASE_URL)
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()


async def init_db() -> None:
    async with get_db() as db:
        with open("app/db/migrations/001_init.sql", encoding="utf-8") as f:
            await db.executescript(f.read())
        await db.commit()