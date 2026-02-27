import pytest

from app.errors import ProviderError
from app.providers.exchangerate_api import ExchangeRateApiProvider


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    async def json(self):
        return self._payload

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class _FakeSession:
    def __init__(self, payload):
        self._payload = payload

    def get(self, url, timeout):
        return _FakeResponse(self._payload)


@pytest.mark.asyncio
async def test_get_latest_requires_api_key():
    provider = ExchangeRateApiProvider(
        http_session=_FakeSession({}),
        api_key=None,
        base_url="https://v6.exchangerate-api.com/v6",
        timeout_seconds=1.0,
    )
    with pytest.raises(ProviderError):
        await provider.get_latest(base="USD")


@pytest.mark.asyncio
async def test_get_latest_parses_success_payload():
    payload = {
        "result": "success",
        "conversion_rates": {"usd": 1.0, "eur": 0.92},
    }
    provider = ExchangeRateApiProvider(
        http_session=_FakeSession(payload),
        api_key="key",
        base_url="https://v6.exchangerate-api.com/v6",
        timeout_seconds=1.0,
    )
    rates = await provider.get_latest(base="USD")
    assert rates == {"USD": 1.0, "EUR": 0.92}


@pytest.mark.asyncio
async def test_get_latest_handles_provider_error_payload():
    payload = {"result": "error", "error-type": "invalid-key"}
    provider = ExchangeRateApiProvider(
        http_session=_FakeSession(payload),
        api_key="key",
        base_url="https://v6.exchangerate-api.com/v6",
        timeout_seconds=1.0,
    )
    with pytest.raises(ProviderError):
        await provider.get_latest(base="USD")
