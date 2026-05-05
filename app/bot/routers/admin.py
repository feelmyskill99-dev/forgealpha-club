from aiogram import Router, types
from aiogram.filters import Command

from app.core.config import settings
from app.services.payments import confirm_invoice

router = Router()


@router.message(Command("admin"))
async def cmd_admin(message: types.Message) -> None:
    user = message.from_user
    if user is None or user.id != settings.ADMIN_ID:
        return

    await message.answer(
        "Admin commands:\n"
        "/confirm_payment <payment_id> <user_id> <tier> [tx_hash]\n"
        "/add_signal <title> | <description> | [source] | [min_tier]"
    )


@router.message(Command("confirm_payment"))
async def cmd_confirm_payment(message: types.Message) -> None:
    user = message.from_user
    if user is None or user.id != settings.ADMIN_ID:
        return

    parts = (message.text or "").split()
    if len(parts) < 4:
        await message.answer("Формат: /confirm_payment <payment_id> <user_id> <tier> [tx_hash]")
        return

    payment_id = int(parts[1])
    user_id = int(parts[2])
    tier = int(parts[3])
    tx_hash = parts[4] if len(parts) > 4 else None

    await confirm_invoice(payment_id=payment_id, user_id=user_id, tier=tier, tx_hash=tx_hash)
    await message.answer(f"Платёж {payment_id} подтверждён. Пользователь {user_id} получил tier {tier}.")
