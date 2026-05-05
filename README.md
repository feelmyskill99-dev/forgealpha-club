# ForgeAlpha Club — On-Chain Intelligence Bot

**Professional crypto analytics platform powered by real-time blockchain data, wallet tracking, and public market signals.**

> **GitHub**: https://github.com/feelmyskill99-dev/forgealpha-club  
> **Version**: 2.0 (Modular Architecture)

---

## 🚀 What is ForgeAlpha Club?

ForgeAlpha Club is a **legal and transparent crypto intelligence tool** that helps traders and analysts get faster access to:

- Real-time on-chain activity (new pools, large wallet movements, smart money flows)
- Public market signals and volume spikes
- Wallet performance tracking and analytics
- Aggregated public information from open sources

We do **not** sell private information, insider tips, or confidential data. All signals are derived from publicly available blockchain data, public APIs, and open social channels.

---

## ✨ Key Features (v2)

- **Tier-based access** with time advantage (0–60 seconds delay)
- **Real-time on-chain scanner** (mock for demo, ready for Helius/QuickNode)
- **Secure payment flow** (pending → confirmed, no instant upgrades)
- **Referral system** with real rewards only after confirmed payment
- **Modular architecture** (easy to extend and maintain)
- **Production-ready structure** (Docker, CI, migrations, tests)

---

## 💎 Subscription Tiers

| Tier          | Price          | Delay | What you get |
|---------------|----------------|-------|--------------|
| **Free**      | Free           | 60s   | Basic on-chain alerts |
| **Basic**     | $100 / 0.5 SOL | 30s   | Faster signals + wallet tracking |
| **VIP**       | $150 / 1 SOL   | 5s    | Priority signals + advanced analytics |
| **Pro**       | Custom         | 0s    | Full access + API + revenue share (by invitation) |

---

## 🛠️ Quick Start (Local Development)

```bash
git clone https://github.com/feelmyskill99-dev/forgealpha-club.git
cd forgealpha-club

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env with your BOT_TOKEN and ADMIN_ID

python -m app.main
```

---

## 📁 Project Structure (v2)

```
forgealpha-club/
├── app/
│   ├── main.py
│   ├── core/              # Configuration, logging, constants
│   ├── bot/               # Telegram bot routers & handlers
│   ├── db/                # Database connection + repositories + migrations
│   ├── services/          # Business logic (payments, subscriptions, signals)
│   ├── scanners/          # On-chain scanners (mock + real)
│   └── utils/
├── tests/
├── scripts/
├── .github/workflows/
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── requirements.txt
```

---

## 🔒 Security & Compliance Notes

- All payments go through **pending → confirmed** flow only
- No instant tier upgrades without verified transaction
- HTML escaping enabled for all user-generated content
- Rate limiting and input validation on all endpoints
- Clear separation between public on-chain data and any paid features

**Legal positioning**: This product provides **on-chain analytics and public market intelligence**. It does not provide or sell non-public information.

---

## 🧪 Testing

```bash
pytest
ruff check .
mypy app/
```

---

## 🐳 Docker

```bash
docker-compose up --build
```

---

## 📈 Roadmap

- [x] Modular architecture (v2)
- [x] Secure payment flow
- [ ] Real Helius/QuickNode scanner integration
- [ ] PostgreSQL + Alembic migrations
- [ ] Full referral system with confirmed payments only
- [ ] Web dashboard (FastAPI + HTMX)
- [ ] NFT subscription option
- [ ] CI/CD + automated tests

---

## ⚠️ Important

This is **demo software**. Real payments are not processed.  
For production use, implement proper Solana transaction verification (Helius, QuickNode, or Solana RPC).

**Not financial advice.** Cryptocurrency trading involves significant risk.

---

## 🤝 Contributing

Pull requests are welcome. Please follow the modular structure and add tests for new features.

---

**ForgeAlpha Club v2** — Clean. Modular. Legal-safe. Ready for growth.