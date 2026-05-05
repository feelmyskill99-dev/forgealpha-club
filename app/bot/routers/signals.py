from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.core.config import settings
from app.db.repositories.signals import add_signal, get_recent_signals

router = Router()


@router.message(Command("signals"))
async def cmd_signals(message: types.Message) -> None:
    signals = await get_recent_signals(limit=5)

    if not signals:
        await message.answer("Пока нет свежих сигналов.")
        return

    text = "\n\n".join(
        f"📡 {signal['title']}\n{signal['description']}"
        for signal in signals
    )
    await message.answer(text)


@router.callback_query(lambda callback: callback.data == "signals")
async def callback_signals(callback: CallbackQuery) -> None:
    signals = await get_recent_signals(limit=5)

    if not signals:
        text = "Пока нет свежих сигналов."
    else:
        text = "\n\n".join(
            f"📡 {signal['title']}\n{signal['description']}"
            for signal in signals
        )

    message = callback.message

    if isinstance(message, Message):
        await message.answer(text)
    else:
        await callback.answer(text, show_alert=True)

    await callback.answer()


@router.message(Command("add_signal"))
async def cmd_add_signal(message: types.Message) -> None:
    user = message.from_user
    if user is None or user.id != settings.ADMIN_ID:
        return

    parts = (message.text or "").split(maxsplit=2)

    if len(parts) < 3:
        await message.answer(
            "Использование:\n"
            "/add_signal <title> <description>"
        )
        return

    title = parts[1]
    description = parts[2]

    signal_id = await add_signal(
        title=title,
        description=description,
        source="admin",
        min_tier=0,
    )

    await message.answer(f"Сигнал создан. ID: {signal_id}")
