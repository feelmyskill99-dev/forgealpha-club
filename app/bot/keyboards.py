from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.core.config import settings
from app.core.constants import TIER_NAMES, Tier


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📡 Latest signals", callback_data="signals")],
            [InlineKeyboardButton(text="💳 Subscribe", callback_data="subscribe")],
        ]
    )


def subscribe_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"🟢 {TIER_NAMES[Tier.BASIC]} — ${settings.TIER_PRICES[Tier.BASIC]}",
                    callback_data="buy_1",
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"🔵 {TIER_NAMES[Tier.VIP]} — ${settings.TIER_PRICES[Tier.VIP]}",
                    callback_data="buy_2",
                )
            ],
            [InlineKeyboardButton(text="⬅️ Back", callback_data="main_menu")],
        ]
    )
