import os
from pathlib import Path

os.environ.setdefault("ENV", "test")
os.environ.setdefault("BOT_TOKEN", "123456:test")
os.environ.setdefault("ADMIN_ID", "123456789")
os.environ.setdefault("PAYMENT_WALLET", "test_wallet")
os.environ.setdefault("DATABASE_URL", "forgealpha_test.db")

import pytest  # noqa: E402

from app.db.connection import init_db  # noqa: E402


@pytest.fixture(autouse=True)
async def setup_test_database() -> None:
    db_path = Path("forgealpha_test.db")

    if db_path.exists():
        db_path.unlink()

    await init_db()

    yield

    if db_path.exists():
        db_path.unlink()