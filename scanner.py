import asyncio
import random
from datetime import datetime
from database import add_signal
from config import MOCK_SIGNALS

# Симуляция ончейн-сканера (в реальности: Helius/QuickNode WebSocket + фильтры по кошелькам)
# Отслеживает "успешные" кошельки, новые пулы Pump.fun/Raydium и т.д.

async def simulate_onchain_scanner():
    """Фоновая задача: каждые 45-90 секунд генерирует 'реальный' ончейн-сигнал для tier 1"""
    while True:
        await asyncio.sleep(random.randint(45, 90))
        
        # Примеры "реальных" обнаружений
        examples = [
            "🟢 [Ончейн] Кошелёк 9pQ7xK... (winrate 68% за 14 дней) купил $NEWPEPE на $3,850. Мемпул: 12k tx/s",
            "🟢 [Raydium] Новый пул для $MOONSHOT создан. Ликвидность $42k. Кит Wintermute related wallet зашёл на $12k",
            "🟢 [Pump.fun] Токен $ALPHA launched 47 сек назад. 3400 holders уже. Smart money (3 кошелька с 90%+ винрейтом) накупили $8.2k",
            "🟢 [DexScreener alert] $BONK2.0 volume spike +420% за 4 мин. 2 кита из топ-50 добавили позиции.",
        ]
        
        text = random.choice(examples)
        signal_id = await add_signal(text, min_tier=1, source="onchain_scanner")
        print(f"[SCANNER] New on-chain signal #{signal_id} added for tier 1+")
        
        # Иногда добавляем tier 2 "из закрытой группы"
        if random.random() > 0.6:
            kols = [
                "🔵 [KOL Group • @cryptoking] Ребята, проект $ZETA делает stealth launch через 25 мин. Только для держателей их предыдущего NFT. Не пабликуйте.",
                "🔵 [Private Alpha Chat] Маркет-мейкер Gotbit начал накапливать $SOLX. Объявление о листинге на Bybit через 48ч.",
            ]
            text2 = random.choice(kols)
            await add_signal(text2, min_tier=2, source="kol_group")
            print(f"[SCANNER] KOL signal added for tier 2+")

async def seed_initial_signals():
    """Добавляет начальные примеры сигналов при старте"""
    for sig in MOCK_SIGNALS:
        await add_signal(sig["text"], sig["min_tier"], source="seed")
    print("[DB] Initial mock signals seeded")