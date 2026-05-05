import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))  # Твой Telegram ID для админ-команд

# Mock payment address (Solana для примера)
PAYMENT_WALLET = "YourSolanaWalletAddressHereForMockPayments"

# Tiers configuration
TIERS = {
    0: {"name": "Демо", "price": 0, "delay": 60, "description": "Базовые сигналы с задержкой 60 сек (ончейн-аналитика)"},
    1: {"name": "Базовый", "price": 100, "delay": 30, "description": "Сигналы с задержкой 30 сек + ончейн-альфа"},
    2: {"name": "VIP", "price": 150, "delay": 5, "description": "Сигналы из закрытых групп с задержкой 5 сек + KOL-инсайды"},
    3: {"name": "Inner Circle", "price": 0, "delay": 0, "description": "Полный доступ без задержек + revenue share (только по приглашению)"}
}

# Mock signals examples (в реальном - из сканера и скаутов)
MOCK_SIGNALS = [
    {"text": "🟢 Кошелёк 7xK9pQ... (70% винрейт за неделю) только что купил $TOKEN на $4,200. Памп в мемпуле!", "min_tier": 1},
    {"text": "🔵 [Закрытая группа KOL] Проект X запускает токен через 45 мин. Пресейл для NFT-холдеров. Инфа до паблика.", "min_tier": 2},
    {"text": "🟣 [Inner] Маркет-мейкер DWF Labs завёл 750k USDT на ордербук Y. Листинг на OKX через 36 часов.", "min_tier": 3},
]