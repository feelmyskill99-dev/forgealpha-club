from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

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
    migration_path = Path("app/db/migrations/001_init.sql")
    async with get_db() as db:
        await db.executescript(migration_path.read_text(encoding="utf-8"))
        await db.commit()
