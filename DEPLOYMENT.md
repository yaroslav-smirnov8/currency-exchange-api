# Deployment & Local Run Guide

This project is an `aiohttp` REST API that provides currency exchange rates and conversion.

## Prerequisites

- **Python**: use **3.11 or 3.12**.
  - This repository currently pins `aiohttp==3.8.3` in `requirements.txt`. That version may not be compatible with Python 3.13+.
- Internet access (only if you use the real provider).
- An ExchangeRate-API key (only if you use the real provider).

## 1) Create and activate a virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 2) Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3) Configure environment variables

Create/update a `.env` file in the project root (next to `main.py`).

Recommended `.env` template:

```dotenv
API_PROVIDER=exchangerate_api
EXCHANGERATE_API_KEY=YOUR_KEY_HERE
EXCHANGERATE_BASE_URL=https://v6.exchangerate-api.com/v6
HTTP_TIMEOUT_SECONDS=8.0

CORS_ENABLED=true
CORS_ALLOWED_ORIGINS=*
```

Provider selection:

- `API_PROVIDER=exchangerate_api` uses the real ExchangeRate-API provider.
- `API_PROVIDER=mock` uses an in-memory provider and does not require a key.

Security note:

- Do not commit real secrets into `.env`. If an API key was exposed, rotate it in the provider dashboard.

## 4) Run the application

```powershell
python main.py
```

Default address:

- `http://localhost:8080`

## 5) Test the API without Postman (curl)

Health check:

```powershell
curl http://localhost:8080/healthz
```

Convert:

```powershell
curl "http://localhost:8080/v1/convert?base=USD&quote=EUR&amount=10"
```

Latest rates:

```powershell
curl "http://localhost:8080/v1/rates/USD?symbols=EUR,GBP"
```

## 6) Do you need Postman?

No. Postman is optional. It is useful for:

- saving requests as a collection,
- sharing examples,
- checking responses quickly while developing.

## 7) Postman setup guide

### 7.1 Create an environment

1. Open Postman → Environments → Create Environment.
2. Add a variable:
   - `base_url` = `http://localhost:8080`
3. Save.

### 7.2 Create a collection

1. Collections → New Collection.
2. Name it `Currency Exchange API`.

### 7.3 Add requests

#### Health check

- Method: `GET`
- URL: `{{base_url}}/healthz`

Expected response:

```json
{ "data": { "status": "ok" } }
```

#### Convert

- Method: `GET`
- URL: `{{base_url}}/v1/convert`
- Params:
  - `base`: `USD`
  - `quote`: `EUR`
  - `amount`: `10`

Expected response (shape):

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

#### Latest rates

- Method: `GET`
- URL: `{{base_url}}/v1/rates/USD`
- Params (optional):
  - `symbols`: `EUR,GBP`

Expected response (shape):

```json
{
  "data": {
    "base": "USD",
    "rates": { "EUR": 0.92, "GBP": 0.79 },
    "provider": "exchangerate_api"
  }
}
```

### 7.4 Common error responses

Validation error example (bad currency code):

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid currency code format.",
    "details": { "field": "base", "expected": "ISO-4217" }
  }
}
```

## 8) Widget embedding note (CORS)

If this API is called from a widget running in a browser, configure CORS:

- For development you can keep `CORS_ALLOWED_ORIGINS=*`.
- For production, set `CORS_ALLOWED_ORIGINS` to a comma-separated list of trusted origins, for example:

```dotenv
CORS_ALLOWED_ORIGINS=https://partner1.com,https://partner2.com
```

