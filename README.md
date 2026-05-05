# ForgeAlpha Club — On-Chain Intelligence Bot

ForgeAlpha Club is a Telegram bot prototype for public crypto market monitoring, on-chain activity alerts, and subscription-based signal delivery.

The project is designed as legal-safe demo software. It does **not** sell private information, insider tips, confidential data, NDA-protected material, or non-public listing information.

## Features

- Telegram bot based on aiogram 3
- SQLite storage via aiosqlite
- Modular architecture: bot routers, services, repositories, scanners, jobs
- Subscription tiers with delayed signal delivery
- Pending payment invoices with manual confirmation flow
- Mock scanner for demo on-chain events
- Jobs for subscription expiration and payment checking placeholder
- Tests, linting, type checking, Docker and GitHub Actions CI

## Project structure

```text
app/
  bot/
    routers/
      admin.py
      signals.py
      start.py
      subscribe.py
    keyboards.py
    messages.py
  core/
    config.py
    constants.py
    logging.py
  db/
    connection.py
    migrations/001_init.sql
    repositories/
      payments.py
      signals.py
      users.py
  jobs/
    expire_subscriptions.py
    payment_checker.py
  scanners/
    base.py
    mock_scanner.py
  services/
    payments.py
    signal_delivery.py
    subscriptions.py
scripts/
  init_db.py
  run_bot.ps1
  run_bot.sh
  run_mock_scanner.py
tests/
```

## Local setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python scripts/init_db.py
pytest
ruff check .
mypy app/
```

## Run bot

```powershell
.\scripts\run_bot.ps1
```

Linux/macOS:

```bash
bash scripts/run_bot.sh
```

## Demo flow

1. Initialize database: `python scripts/init_db.py`
2. Run mock scanner: `python scripts/run_mock_scanner.py`
3. Start bot: `python -m app.main`
4. User creates invoice through subscription menu
5. Admin confirms invoice:

```text
/confirm_payment <payment_id> <user_id> <tier> [tx_hash]
```

6. User tier is upgraded only after confirmed payment
7. Expired subscriptions can be processed with `expire_subscriptions` job

## Admin commands

```text
/admin
/add_signal <title> | <description> | [source] | [min_tier]
/confirm_payment <payment_id> <user_id> <tier> [tx_hash]
```

## Payment safety

Current implementation is intentionally conservative:

- creating invoice does not upgrade user;
- payment starts as `pending`;
- subscription activates only through explicit confirmation;
- real blockchain verification is not implemented yet;
- payment checker is a safe placeholder.

Before production launch, add a real verifier that checks transaction hash, recipient wallet, amount, currency, confirmations, duplicate usage and expiration.

## CI

GitHub Actions runs:

```bash
ruff check .
pytest
mypy app/
```

## License

MIT or proprietary, depending on your product plan.
