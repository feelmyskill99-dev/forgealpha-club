from aiogram import Router, types
from aiogram.filters import Command
from app.core.config import settings
from app.services.payments import confirm_payment_and_activate

router = Router()


@router.message(Command("confirm"))
async def cmd_confirm(message: types.Message):
    if message.from_user.id != settings.ADMIN_ID:
        return

    args = message.text.split()
    if len(args) < 3:
        await message.answer("Использование: /confirm <payment_id> <user_id> <tier>")
        return

    payment_id = int(args[1])
    user_id = int(args[2])
    tier = int(args[3])

    await confirm_payment_and_activate(user_id, payment_id, tier)
    await message.answer(f"✅ Платёж {payment_id} подтверждён. Пользователь {user_id} получил tier {tier}")