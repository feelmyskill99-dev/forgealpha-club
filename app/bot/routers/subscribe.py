from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import subscribe_keyboard
from app.services.payments import create_invoice

router = Router()


async def _answer_or_edit(callback: CallbackQuery, text: str) -> None:
    message = callback.message

    if isinstance(message, Message):
        await message.edit_text(text, reply_markup=subscribe_keyboard())
    else:
        await callback.answer(text, show_alert=True)


@router.callback_query(F.data == "subscribe")
async def show_subscribe(callback: CallbackQuery) -> None:
    await _answer_or_edit(
        callback,
        "Choose a subscription tier. Payments are created as pending invoices and require confirmation.",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("buy_"))
async def buy_subscription(callback: CallbackQuery) -> None:
    user = callback.from_user
    data = callback.data

    if user is None or data is None:
        await callback.answer("Invalid request", show_alert=True)
        return

    tier = int(data.split("_", maxsplit=1)[1])
    amount = 49.0 if tier == 1 else 149.0

    payment_id = await create_invoice(
        user_id=user.id,
        tier=tier,
        amount=amount,
    )

    message = callback.message
    text = (
        "Invoice created.\n\n"
        f"Payment ID: {payment_id}\n"
        f"Amount: ${amount}\n\n"
        "Status: pending confirmation."
    )

    if isinstance(message, Message):
        await message.edit_text(text)
    else:
        await callback.answer(text, show_alert=True)

    await callback.answer()