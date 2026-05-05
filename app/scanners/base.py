from abc import ABC, abstractmethod
from typing import Any


class BaseScanner(ABC):
    @abstractmethod
    async def scan(self) -> list[dict[str, Any]]:
        """Return a list of detected public market/on-chain signals."""
        raise NotImplementedError

    async def run_once(self) -> None:
        await self.scan()
