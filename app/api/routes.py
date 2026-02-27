from __future__ import annotations

import re

from aiohttp import web

from app.errors import ValidationError, json_response
from app.services.exchange_service import ExchangeService


_CURRENCY_RE = re.compile(r"^[A-Z]{3}$")


def _parse_currency(value: str | None, *, field: str) -> str:
    if not value:
        raise ValidationError("Missing required parameter.", details={"field": field})
    normalized = value.strip().upper()
    if not _CURRENCY_RE.match(normalized):
        raise ValidationError("Invalid currency code format.", details={"field": field, "expected": "ISO-4217"})
    return normalized


def _parse_amount(value: str | None) -> float:
    if not value:
        raise ValidationError("Missing required parameter.", details={"field": "amount"})
    try:
        amount = float(value.replace(",", "."))
    except ValueError as exc:
        raise ValidationError("Amount must be a number.", details={"field": "amount"}) from exc
    if amount <= 0:
        raise ValidationError("Amount must be greater than zero.", details={"field": "amount"})
    return amount


async def healthz(request: web.Request) -> web.Response:
    return json_response({"status": "ok"})


async def convert(request: web.Request) -> web.Response:
    base = _parse_currency(request.query.get("base"), field="base")
    quote = _parse_currency(request.query.get("quote"), field="quote")
    if base == quote:
        raise ValidationError("Base and quote currencies must be different.")
    amount = _parse_amount(request.query.get("amount"))

    service: ExchangeService = request.app["exchange_service"]
    result = await service.convert(base=base, quote=quote, amount=amount)
    return json_response(result)


async def latest_rates(request: web.Request) -> web.Response:
    base = _parse_currency(request.match_info.get("base"), field="base")
    symbols_raw = request.query.get("symbols")
    symbols = None
    if symbols_raw:
        symbols = [_parse_currency(s, field="symbols") for s in symbols_raw.split(",")]

    service: ExchangeService = request.app["exchange_service"]
    result = await service.latest_rates(base=base, symbols=symbols)
    return json_response(result)


async def options_handler(request: web.Request) -> web.Response:
    return web.Response(status=204)


def register_routes(app: web.Application) -> None:
    app.router.add_get("/healthz", healthz)
    app.router.add_get("/v1/convert", convert)
    app.router.add_get("/v1/rates/{base}", latest_rates)
    app.router.add_route("OPTIONS", "/{tail:.*}", options_handler)
