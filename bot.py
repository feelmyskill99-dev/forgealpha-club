import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from config import BOT_TOKEN, ADMIN_ID, TIERS, PAYMENT_WALLET
from database import (
    init_db, get_user, create_or_update_user, upgrade_user_tier,
    add_signal, get_active_users_by_tier, add_payment
)
from scanner import simulate_onchain_scanner, seed_initial_signals

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Глобальный флаг для остановки
running = True

async def send_signal_to_user(user_id: int, text: str, delay: int = 0):
    """Отправляет сигнал с задержкой (симуляция tier-based delay)"""
    if delay > 0:
        await asyncio.sleep(delay)
    try:
        await bot.send_message(
            user_id,
            f"📡 <b>ALPHA SIGNAL</b>\n\n{text}\n\n"
            f"<i>Время: {datetime.now().strftime('%H:%M:%S')}</i>\n"
            f"<i>Не финансовый совет • DYOR</i>",
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"Failed to send to {user_id}: {e}")

async def broadcast_signal(signal_text: str, min_tier: int, base_delay: int = 0):
    """Рассылает сигнал по всем активным пользователям с учётом их tier и задержки"""
    users = await get_active_users_by_tier(min_tier)
    logger.info(f"Broadcasting signal (min_tier={min_tier}) to {len(users)} users")
    
    for user_id in users:
        user = await get_user(user_id)
        if not user:
            continue
        
        user_delay = TIERS.get(user["tier"], TIERS[0])["delay"]
        # Высшие тиеры получают быстрее (меньше задержка)
        actual_delay = max(0, user_delay - base_delay)  # base_delay от источника
        
        asyncio.create_task(send_signal_to_user(user_id, signal_text, actual_delay))

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.full_name
    
    # Проверка реферала (простая: /start ref123)
    ref = None
    if message.text and " " in message.text:
        parts = message.text.split()
        if len(parts) > 1 and parts[1].startswith("ref"):
            try:
                ref = int(parts[1][3:])
            except:
                pass
    
    await create_or_update_user(user_id, username, ref)
    user = await get_user(user_id)
    
    if ref and ref != user_id:
        # Начисляем рефералу +1 (упрощённо)
        pass  # В реальности: UPDATE referrals +1 и проверить на бонусы
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Мой статус", callback_data="status")],
        [InlineKeyboardButton(text="💎 Подписаться / Улучшить", callback_data="subscribe")],
        [InlineKeyboardButton(text="📡 Последние сигналы", callback_data="latest_signals")],
        [InlineKeyboardButton(text="ℹ️ Как это работает", callback_data="how_it_works")]
    ])
    
    await message.answer(
        f"👋 <b>Добро пожаловать в ForgeAlpha Club!</b>\n\n"
        f"Твой текущий уровень: <b>{TIERS[user['tier']]['name']}</b>\n"
        f"Задержка сигналов: <b>{TIERS[user['tier']]['delay']} сек</b>\n\n"
        f"Мы продаём не просто инфу — мы продаём <b>время и контекст</b>.\n"
        f"Чистая ончейн-альфа + полузакрытые источники.\n\n"
        f"Выбери действие:",
        reply_markup=kb
    )

@dp.callback_query(F.data == "status")
async def cb_status(callback: types.CallbackQuery):
    user = await get_user(callback.from_user.id)
    if not user:
        await callback.answer("Ошибка. Напиши /start")
        return
    
    tier_info = TIERS[user['tier']]
    until = user.get('subscribed_until') or "Бессрочно (демо)"
    
    text = (
        f"📊 <b>Твой статус в ForgeAlpha Club</b>\n\n"
        f"Уровень: <b>{tier_info['name']}</b> (Tier {user['tier']})\n"
        f"Задержка: <b>{tier_info['delay']} секунд</b>\n"
        f"Подписка до: <b>{until}</b>\n"
        f"Рефералов: <b>{user.get('referrals', 0)}</b>\n\n"
        f"💰 Цена уровня: ${tier_info['price']}/мес или эквивалент в SOL\n\n"
        f"<i>Для Inner Circle (Tier 3) — только по личному инвайту от админа.</i>"
    )
    await callback.message.edit_text(text)
    await callback.answer()

@dp.callback_query(F.data == "subscribe")
async def cb_subscribe(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user = await get_user(user_id)
    current_tier = user['tier'] if user else 0
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🟢 Tier 1 — Базовый (${TIERS[1]['price']}/мес, 30с)", callback_data="buy_1")],
        [InlineKeyboardButton(text=f"🔵 Tier 2 — VIP (${TIERS[2]['price']}/мес, 5с)", callback_data="buy_2")],
        [InlineKeyboardButton(text="🟣 Tier 3 — Inner Circle (по инвайту)", callback_data="inner_info")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="status")]
    ])
    
    await callback.message.edit_text(
        f"💎 <b>Выбери уровень подписки</b>\n\n"
        f"Твой текущий: {TIERS[current_tier]['name']}\n\n"
        f"<b>Как оплатить (mock для демо):</b>\n"
        f"1. Нажми на уровень\n"
        f"2. Переведи SOL/USDT на кошелёк: <code>{PAYMENT_WALLET}</code>\n"
        f"3. Пришли TX hash админу или используй /pay\n\n"
        f"<i>В реальном клубе — автоматическая проверка через Solana RPC + Helius.</i>",
        reply_markup=kb
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("buy_"))
async def cb_buy(callback: types.CallbackQuery):
    tier = int(callback.data.split("_")[1])
    user_id = callback.from_user.id
    
    if tier == 3:
        await callback.answer("Tier 3 только по личному приглашению от @admin. Напиши в поддержку.", show_alert=True)
        return
    
    # Mock payment: сразу апгрейдим (в реальности ждём подтверждения)
    await upgrade_user_tier(user_id, tier)
    await add_payment(user_id, tier, TIERS[tier]['price'])
    
    await callback.message.edit_text(
        f"✅ <b>Подписка Tier {tier} активирована!</b>\n\n"
        f"Теперь твоя задержка: <b>{TIERS[tier]['delay']} сек</b>\n"
        f"Ты будешь получать сигналы на {TIERS[tier]['delay']} секунд раньше массы.\n\n"
        f"Спасибо за доверие к ForgeAlpha Club.\n"
        f"Сигналы начнут приходить автоматически."
    )
    await callback.answer("Подписка активирована!")

@dp.callback_query(F.data == "inner_info")
async def cb_inner(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🟣 <b>Inner Circle — эксклюзив</b>\n\n"
        "Это уровень для тех, кто готов делиться прибылью (revenue share 15-25%) "
        "в обмен на полный доступ без задержек и прямые инсайды от команд.\n\n"
        "Условия:\n"
        "• Личное приглашение от текущего участника или админа\n"
        "• Минимум $5k+ в портфеле или доказанный трек-рекорд\n"
        "• NDA + revenue share agreement\n\n"
        "Напиши @admin с темой 'Inner Circle application'."
    )
    await callback.answer()

@dp.callback_query(F.data == "how_it_works")
async def cb_how(callback: types.CallbackQuery):
    text = (
        "ℹ️ <b>Как работает ForgeAlpha Club</b>\n\n"
        "<b>Уровень 1 (Чистая альфа)</b> — ончейн-сканирование мемпула, "
        "отслеживание китов, новых пулов Pump.fun/Raydium. "
        "Ты получаешь сигнал на 30 сек раньше DexScreener.\n\n"
        "<b>Уровень 2 (Платные группы)</b> — сигналы из закрытых Discord/Telegram KOL-чатов, "
        "пресейлы, накопления маркет-мейкеров.\n\n"
        "<b>Уровень 3 (Inner)</b> — прямые инсайды от команд, листинги, "
        "эирдропы, токеномика. Только для избранных.\n\n"
        "<b>Этика:</b> Мы не сливаем уязвимости и не участвуем в кражах. "
        "Только публичные/полузакрытые данные + скорость."
    )
    await callback.message.edit_text(text)
    await callback.answer()

@dp.callback_query(F.data == "latest_signals")
async def cb_latest(callback: types.CallbackQuery):
    # Показываем последние 3 сигнала (в реальности из БД)
    await callback.message.edit_text(
        "📡 <b>Последние сигналы (демо)</b>\n\n"
        "1. 🟢 [Ончейн] Кошелёк 9pQ7xK... купил $NEWPEPE на $3,850\n"
        "2. 🔵 [KOL] Проект $ZETA stealth launch через 25 мин\n"
        "3. 🟣 [Inner] DWF Labs завёл 750k USDT на $SOLX\n\n"
        "<i>Полные сигналы приходят автоматически в зависимости от твоего tier.</i>"
    )
    await callback.answer()

@dp.message(Command("add_signal"))
async def cmd_add_signal(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Только для админа.")
        return
    
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer("Использование: /add_signal <min_tier> <текст сигнала>")
        return
    
    try:
        min_tier = int(args[1])
        text = args[2]
    except:
        await message.answer("min_tier должен быть числом 1-3")
        return
    
    signal_id = await add_signal(text, min_tier)
    await message.answer(f"✅ Сигнал #{signal_id} добавлен для tier {min_tier}+")
    
    # Немедленная рассылка
    await broadcast_signal(text, min_tier)

@dp.message(Command("pay"))
async def cmd_pay(message: types.Message):
    """Mock оплата: /pay 1 0.5SOL txhash123"""
    args = message.text.split()
    if len(args) < 3:
        await message.answer("Использование: /pay <tier> <amount> [tx_hash]")
        return
    
    tier = int(args[1])
    amount = float(args[2])
    tx = args[3] if len(args) > 3 else "mock_tx_" + str(int(datetime.now().timestamp()))
    
    user_id = message.from_user.id
    await add_payment(user_id, tier, amount, tx)
    await upgrade_user_tier(user_id, tier)
    
    await message.answer(
        f"✅ Оплата принята! Tier {tier} активирован.\n"
        f"Сумма: ${amount} | TX: {tx[:20]}...\n"
        f"Теперь твоя задержка: {TIERS[tier]['delay']} сек"
    )

@dp.message(Command("stats"))
async def cmd_stats(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    # Простая статистика
    users = await get_active_users_by_tier(0)
    await message.answer(f"📈 Активных пользователей: {len(users)}\n(демо-версия)")

async def main():
    await init_db()
    await seed_initial_signals()
    
    # Запускаем фоновый сканер
    asyncio.create_task(simulate_onchain_scanner())
    
    logger.info("ForgeAlpha Club Bot started!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())