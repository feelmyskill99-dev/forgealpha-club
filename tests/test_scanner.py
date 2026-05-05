import pytest

from app.db.repositories.signals import get_recent_signals
from app.scanners.mock_scanner import run_mock_scanner_once


@pytest.mark.asyncio
async def test_mock_scanner_creates_signal() -> None:
    await run_mock_scanner_once()

    signals = await get_recent_signals(limit=5)
    assert len(signals) == 1
    assert signals[0]["source"] == "mock"
