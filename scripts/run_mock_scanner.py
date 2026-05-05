import asyncio

from app.db.connection import init_db
from app.scanners.mock_scanner import run_mock_scanner_once


async def main() -> None:
    await init_db()
    await run_mock_scanner_once()
    print("Mock scanner completed")


if __name__ == "__main__":
    asyncio.run(main())
