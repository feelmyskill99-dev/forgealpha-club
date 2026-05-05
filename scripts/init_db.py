import asyncio
from app.db.connection import init_db
from app.core.logging import logger


async def main():
    await init_db()
    logger.info("Database initialized successfully")


if __name__ == "__main__":
    asyncio.run(main())