# Currency Exchange API

Async aiohttp REST API for real-time currency exchange rates and currency conversion.

Designed as a small production-style service:

- **Async I/O-first** (external provider calls are I/O-bound)
- **Clear module boundaries**: routes → service → provider
- **Pluggable providers** (real provider + mock provider for local dev/tests)
- **Consistent JSON contract** for both success and errors
- **Strict input validation** (currency codes, amount parsing)

---

## Why this project

Many client apps (frontend widgets, partner integrations, internal tools) need currency conversion, but should not embed provider-specific details (API keys, response formats, error cases). This API provides a stable contract and hides provider complexity behind an adapter.

---

## Features

- Real-time conversion and latest rates
- Provider abstraction (Protocol-based) with a deterministic **mock** provider
- CORS middleware for browser/widget usage (wildcard or allowlist)
- Timeout handling for external API calls
- Deterministic error model with correct HTTP status codes
- Unit + integration tests

---

## Architecture (high level)

**Request flow**

1. **Routes** validate and normalize input (ISO-4217 currency code format, amount parsing)
2. **Service layer** executes business logic (conversion, symbols filtering)
3. **Provider layer** fetches upstream rates (real provider) or returns deterministic test data (mock)
4. **Middleware** enforces a consistent JSON error schema and handles CORS

**Lifecycle**

The app creates a single `aiohttp.ClientSession` on startup and closes it on cleanup.

---

## API contract

### Response envelopes

- Success: `{"data": ...}`
- Error: `{"error": {"code": ..., "message": ..., "details": ...}}`

This contract is implemented in `app/errors.py` and applied uniformly via middleware.

---

## Endpoints + examples

### Health

```http
GET /healthz
```

```json
{
  "data": {
    "status": "ok"
  }
}
```

### Convert

```http
GET /v1/convert?base=USD&quote=EUR&amount=10
```

```json
{
  "data": {
    "base": "USD",
    "quote": "EUR",
    "amount": 10.0,
    "rate": 0.92,
    "result": 9.2,
    "provider": "exchangerate_api"
  }
}
```

> Note: `rate` and `result` depend on the selected provider and current market data; the schema is stable.

### Latest rates

```http
GET /v1/rates/USD?symbols=EUR,GBP
```

Example response shape:

```json
{
  "data": {
    "base": "USD",
    "rates": {
      "EUR": 0.92,
      "GBP": 0.79
    },
    "provider": "exchangerate_api"
  }
}
```

### Validation error example

```http
GET /v1/convert?base=USDT&quote=EUR&amount=10
```

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid currency code format.",
    "details": {
      "field": "base",
      "expected": "ISO-4217"
    }
  }
}
```

### Provider error example (timeout/upstream failure)

```json
{
  "error": {
    "code": "provider_error",
    "message": "External provider request failed or timed out."
  }
}
```

---

## Repository structure (actual)

```text
.
├── app/
│   ├── api/
│   │   ├── middlewares.py
│   │   └── routes.py
│   ├── providers/
│   │   ├── base.py
│   │   ├── exchangerate_api.py
│   │   └── mock.py
│   ├── services/
│   │   └── exchange_service.py
│   ├── app_factory.py
│   ├── errors.py
│   └── settings.py
├── tests/
├── main.py
├── requirements.txt
└── RUN_INSTRUCTIONS.md
```

---

## Run locally

See `RUN_INSTRUCTIONS.md` for step-by-step commands.

Quick start (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

Default address: `http://localhost:8080`

---

## Environment variables

| Variable | Required | Default | Description |
|---|---:|---|---|
| API_PROVIDER | Yes | exchangerate_api | Provider: `exchangerate_api` or `mock` |
| EXCHANGERATE_API_KEY | Only for `exchangerate_api` | | API key for ExchangeRate-API |
| EXCHANGERATE_BASE_URL | No | https://v6.exchangerate-api.com/v6 | Provider base URL |
| HTTP_TIMEOUT_SECONDS | No | 8.0 | Provider HTTP timeout |
| CORS_ENABLED | No | true | Enable CORS middleware |
| CORS_ALLOWED_ORIGINS | No | * | Comma-separated origins or `*` |

Operational notes:

- Use `API_PROVIDER=mock` for local runs/tests without external dependencies.
- In production, prefer a strict allowlist in `CORS_ALLOWED_ORIGINS`.

---

## Testing

```powershell
pytest -q
```

Test suite covers:

- Route-level validation
- Service-layer conversion logic
- Provider integration behavior
- HTTP integration tests for endpoints

---

## Non-goals / constraints

- No DB/persistence (provider is the source of truth)
- No caching layer included by default (can be added if rate limits become a concern)
- No automatic provider failover (provider choice is explicit via `API_PROVIDER`)

---

## License

MIT License
