import pytest

from app.db.repositories.signals import add_signal, get_recent_signals


@pytest.mark.asyncio
async def test_add_and_get_signal() -> None:
    signal_id = await add_signal("Title", "Description", source="test", min_tier=0)
    assert signal_id > 0

    signals = await get_recent_signals(limit=1)
    assert len(signals) == 1
    assert signals[0]["title"] == "Title"
