from __future__ import annotations

from dataclasses import dataclass, field

from app.errors import ProviderError


@dataclass(slots=True)
class MockExchangeRateProvider:
    rates: dict[str, dict[str, float]] = field(
        default_factory=lambda: {
            "USD": {"EUR": 0.92, "GBP": 0.79, "USD": 1.0},
            "EUR": {"USD": 1.09, "GBP": 0.86, "EUR": 1.0},
        }
    )

    async def get_latest(self, *, base: str) -> dict[str, float]:
        try:
            return dict(self.rates[base])
        except KeyError as exc:
            raise ProviderError("Mock provider has no rates for base currency.", details={"base": base}) from exc

    async def get_rate(self, *, base: str, quote: str) -> float:
        rates = await self.get_latest(base=base)
        try:
            return rates[quote]
        except KeyError as exc:
            raise ProviderError("Mock provider has no rate for quote currency.", details={"quote": quote}) from exc

