from aiogram import Router, types
from aiogram.filters import Command
from app.services.signal_delivery import send_signal_with_delay
from app.db.repositories.signals import get_recent_signals

router = Router()


@router.message(Command("signals"))
async def cmd_signals(message: types.Message):
    signals = await get_recent_signals(3)
    text = "📡 <b>Последние сигналы</b>\n\n"
    for s in signals:
        text += f"• {s['text'][:80]}...\n"
    await message.answer(text)


@router.message(Command("add_signal"))
async def cmd_add_signal(message: types.Message):
    # Только для админа (упрощённо)
    if message.from_user.id != settings.ADMIN_ID:
        return
    # ... логика добавления сигнала и рассылки
    await message.answer("Сигнал добавлен (демо)")