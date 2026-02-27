import pytest

from app.errors import ProviderError
from app.providers.mock import MockExchangeRateProvider
from app.services.exchange_service import ExchangeService


@pytest.mark.asyncio
async def test_convert_returns_expected_payload():
    service = ExchangeService(provider=MockExchangeRateProvider(), provider_name="mock")
    result = await service.convert(base="USD", quote="EUR", amount=10.0)
    assert result["base"] == "USD"
    assert result["quote"] == "EUR"
    assert result["amount"] == 10.0
    assert result["rate"] == 0.92
    assert result["result"] == pytest.approx(9.2)
    assert result["provider"] == "mock"


@pytest.mark.asyncio
async def test_latest_rates_filters_symbols():
    service = ExchangeService(provider=MockExchangeRateProvider(), provider_name="mock")
    result = await service.latest_rates(base="USD", symbols=["EUR"])
    assert result["rates"] == {"EUR": 0.92}


@pytest.mark.asyncio
async def test_latest_rates_missing_symbol_raises_provider_error():
    service = ExchangeService(provider=MockExchangeRateProvider(), provider_name="mock")
    with pytest.raises(ProviderError):
        await service.latest_rates(base="USD", symbols=["JPY"])
