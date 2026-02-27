from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any

from aiohttp import ClientSession

from app.errors import ProviderError


@dataclass(frozen=True, slots=True)
class ExchangeRateApiProvider:
    http_session: ClientSession
    api_key: str | None
    base_url: str
    timeout_seconds: float = 8.0

    async def get_latest(self, *, base: str) -> dict[str, float]:
        if not self.api_key:
            raise ProviderError("Provider API key is not configured.")

        url = f"{self.base_url}/{self.api_key}/latest/{base}"
        try:
            async with self.http_session.get(url, timeout=self.timeout_seconds) as resp:
                payload: dict[str, Any] = await resp.json()
        except asyncio.TimeoutError as exc:
            raise ProviderError("Provider request timed out.") from exc
        except Exception as exc:
            raise ProviderError("Provider request failed.") from exc

        if payload.get("result") != "success":
            raise ProviderError("Provider returned an error.", details={"provider_message": payload.get("error-type")})

        rates = payload.get("conversion_rates")
        if not isinstance(rates, dict):
            raise ProviderError("Provider response format is invalid.")

        normalized: dict[str, float] = {}
        for k, v in rates.items():
            if isinstance(k, str) and isinstance(v, (int, float)):
                normalized[k.upper()] = float(v)
        return normalized

    async def get_rate(self, *, base: str, quote: str) -> float:
        rates = await self.get_latest(base=base)
        try:
            return rates[quote]
        except KeyError as exc:
            raise ProviderError("Quote currency not available from provider.", details={"quote": quote}) from exc

