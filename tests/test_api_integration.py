import pytest

from app.app_factory import create_app
from app.settings import Settings


def _mock_settings(cors_enabled: bool = False) -> Settings:
    return Settings(
        provider_name="mock",
        exchangerate_api_key=None,
        exchangerate_base_url="https://v6.exchangerate-api.com/v6",
        http_timeout_seconds=1.0,
        cors_enabled=cors_enabled,
        cors_allowed_origins=["*"],
    )


@pytest.mark.asyncio
async def test_healthz_returns_ok(aiohttp_client):
    app = create_app(_mock_settings())
    client = await aiohttp_client(app)
    resp = await client.get("/healthz")
    assert resp.status == 200
    payload = await resp.json()
    assert payload == {"data": {"status": "ok"}}


@pytest.mark.asyncio
async def test_convert_rejects_same_currency(aiohttp_client):
    app = create_app(_mock_settings())
    client = await aiohttp_client(app)
    resp = await client.get("/v1/convert?base=USD&quote=USD&amount=10")
    assert resp.status == 400
    payload = await resp.json()
    assert payload["error"]["code"] == "validation_error"


@pytest.mark.asyncio
async def test_latest_rates_filters_symbols(aiohttp_client):
    app = create_app(_mock_settings())
    client = await aiohttp_client(app)
    resp = await client.get("/v1/rates/USD?symbols=EUR")
    assert resp.status == 200
    payload = await resp.json()
    assert payload["data"]["rates"] == {"EUR": 0.92}


@pytest.mark.asyncio
async def test_cors_header_added_when_enabled(aiohttp_client):
    app = create_app(_mock_settings(cors_enabled=True))
    client = await aiohttp_client(app)
    resp = await client.get("/healthz", headers={"Origin": "http://example.com"})
    assert resp.headers["Access-Control-Allow-Origin"] == "*"
