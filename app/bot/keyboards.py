from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.core.constants import Tier, TIER_NAMES


def main_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Мой статус", callback_data="status")],
        [InlineKeyboardButton(text="💎 Подписка", callback_data="subscribe")],
        [InlineKeyboardButton(text="📡 Сигналы", callback_data="signals")],
    ])


def subscribe_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🟢 {TIER_NAMES[Tier.BASIC]} — ${settings.TIER_PRICES[Tier.BASIC]}", callback_data="buy_1")],
        [InlineKeyboardButton(text=f"🔵 {TIER_NAMES[Tier.VIP]} — ${settings.TIER_PRICES[Tier.VIP]}", callback_data="buy_2")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")],
    ])
