from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from app.bot.keyboards import subscribe_keyboard
from app.bot.messages import SUBSCRIBE_TEXT
from app.services.payments import create_invoice
from app.core.config import settings

router = Router()


@router.callback_query(F.data == "subscribe")
async def cb_subscribe(callback: CallbackQuery):
    await callback.message.edit_text(SUBSCRIBE_TEXT, reply_markup=subscribe_keyboard())


@router.callback_query(F.data.startswith("buy_"))
async def cb_buy(callback: CallbackQuery):
    tier = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    amount = settings.TIER_PRICES[tier]
    payment_id = await create_invoice(user_id, tier, amount)

    text = f"""
✅ Платёж создан (ID: {payment_id})

Переведи <b>${amount}</b> на:
<code>{settings.PAYMENT_WALLET}</code>

После перевода пришли TX hash админу или используй /pay {tier} <tx_hash>
"""
    await callback.message.edit_text(text)
    await callback.answer()