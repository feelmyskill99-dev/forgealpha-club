import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.core.config import settings
from app.core.logging import logger
from app.bot.routers import start, subscribe, admin, signals   # will be created next


async def main():
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Include routers
    dp.include_router(start.router)
    dp.include_router(subscribe.router)
    dp.include_router(admin.router)
    dp.include_router(signals.router)

    logger.info("ForgeAlpha Club v2 started", env=settings.ENV)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())