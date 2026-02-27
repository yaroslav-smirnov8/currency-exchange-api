from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.errors import ProviderError
from app.providers.base import ExchangeRateProvider


@dataclass(frozen=True, slots=True)
class ExchangeService:
    provider: ExchangeRateProvider
    provider_name: str

    async def convert(self, *, base: str, quote: str, amount: float) -> dict[str, Any]:
        rate = await self.provider.get_rate(base=base, quote=quote)
        return {
            "base": base,
            "quote": quote,
            "amount": amount,
            "rate": rate,
            "result": rate * amount,
            "provider": self.provider_name,
        }

    async def latest_rates(self, *, base: str, symbols: list[str] | None) -> dict[str, Any]:
        rates = await self.provider.get_latest(base=base)
        if symbols is not None:
            filtered: dict[str, float] = {}
            for s in symbols:
                try:
                    filtered[s] = rates[s]
                except KeyError as exc:
                    raise ProviderError("Quote currency not available from provider.", details={"quote": s}) from exc
            rates = filtered
        return {"base": base, "rates": rates, "provider": self.provider_name}

