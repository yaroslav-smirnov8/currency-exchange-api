from __future__ import annotations

from typing import Protocol


class ExchangeRateProvider(Protocol):
    async def get_rate(self, *, base: str, quote: str) -> float: ...

    async def get_latest(self, *, base: str) -> dict[str, float]: ...

