from typing import Any

from app.db.repositories.signals import add_signal
from app.scanners.base import BaseScanner


class MockScanner(BaseScanner):
    async def scan(self) -> list[dict[str, Any]]:
        title = "Mock on-chain activity detected"
        description = "Large wallet movement detected in mock scanner."
        source = "mock"
        min_tier = 0

        await add_signal(
            title=title,
            description=description,
            source=source,
            min_tier=min_tier,
        )

        return [
            {
                "title": title,
                "description": description,
                "source": source,
                "min_tier": min_tier,
            }
        ]


async def run_mock_scanner_once() -> None:
    scanner = MockScanner()
    await scanner.run_once()