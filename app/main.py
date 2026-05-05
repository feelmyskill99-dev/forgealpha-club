import asyncio

from aiogram import Bot, Dispatcher

from app.bot.routers import admin, signals, start, subscribe
from app.core.config import settings
from app.core.logging import logger
from app.db.connection import init_db


async def main() -> None:
    await init_db()

    bot = Bot(token=settings.BOT_TOKEN)
    dispatcher = Dispatcher()

    dispatcher.include_router(start.router)
    dispatcher.include_router(subscribe.router)
    dispatcher.include_router(signals.router)
    dispatcher.include_router(admin.router)

    logger.info("bot_started")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())