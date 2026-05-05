from aiogram import Router, types
from aiogram.filters import Command

from app.core.config import settings
from app.db.repositories.signals import get_recent_signals

router = Router()


@router.message(Command("signals"))
async def cmd_signals(message: types.Message) -> None:
    signals = await get_recent_signals(limit=5)

    if not signals:
        await message.answer("No recent signals yet.")
        return

    text = "\n\n".join(
        f"📡 {signal['title']}\n{signal['description']}"
        for signal in signals
    )
    await message.answer(text)


@router.message(Command("add_signal"))
async def cmd_add_signal(message: types.Message) -> None:
    user = message.from_user
    if user is None or user.id != settings.ADMIN_ID:
        return

    await message.answer("Signal creation command is not implemented yet.")