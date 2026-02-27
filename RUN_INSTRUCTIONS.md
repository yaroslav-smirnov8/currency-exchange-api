# How to run the Currency Exchange API

This guide explains the prerequisites and step-by-step instructions to run the project locally.

---

## Prerequisites

### 1) Python

- Version: **Python 3.11 or 3.12**
- Python 3.13+ may not be compatible with the pinned `aiohttp` version.

### 2) Dependencies (see `requirements.txt`)

- `aiohttp==3.8.3` — web framework for async API
- `python-dotenv==0.21.0` — load environment variables from `.env`
- `requests==2.28.1` — HTTP client (used in tools/tests)

### 3) API key (optional)

- Required only for the real provider (**ExchangeRate-API**)
- You can run using the **mock** provider without a key

---

## How startup works (quick overview)

- Entry point: `main.py` calls `create_app()` and starts the server on port `8080`.
- `create_app()` loads settings from `.env` via `Settings.from_env()` and wires middleware.
- Provider is selected via `API_PROVIDER`: `exchangerate_api` (real) or `mock` (test/local).
- For the real provider, `EXCHANGERATE_API_KEY` is required; otherwise the API returns a provider error.
- CORS is controlled by `CORS_ENABLED`; allowed origins are configured via `CORS_ALLOWED_ORIGINS`.

---

## Step-by-step

### Step 1: Create a virtual environment

```powershell
python -m venv .venv
```

### Step 2: Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Create a `.env` file

Create a `.env` file in the project root (next to `main.py`) with the following content:

```dotenv
# Real provider (requires an API key):
API_PROVIDER=exchangerate_api
EXCHANGERATE_API_KEY=YOUR_KEY_HERE
EXCHANGERATE_BASE_URL=https://v6.exchangerate-api.com/v6
HTTP_TIMEOUT_SECONDS=8.0

# CORS settings
CORS_ENABLED=true
CORS_ALLOWED_ORIGINS=*

# For testing without an API key, use the mock provider instead:
# API_PROVIDER=mock
```

Notes:

- You can get a free API key at https://www.exchangerate-api.com/
- If you do not have a key, set `API_PROVIDER=mock`

### Step 5: Run the application

```powershell
python main.py
```

The server will start at: `http://localhost:8080`

---

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /healthz` | Health check |
| `GET /v1/convert?base=USD&quote=EUR&amount=10` | Convert currency |
| `GET /v1/rates/USD?symbols=EUR,GBP` | Latest rates |

---

## Example requests

### Health check

```powershell
curl http://localhost:8080/healthz
```

### Convert 10 USD to EUR

```powershell
curl "http://localhost:8080/v1/convert?base=USD&quote=EUR&amount=10"
```

### Get EUR and GBP rates relative to USD

```powershell
curl "http://localhost:8080/v1/rates/USD?symbols=EUR,GBP"
```

---

## Do you need Postman?

No. Postman is optional. `curl` (or any HTTP client) is enough.

Postman can be useful if you want to:

- save a request collection,
- share requests with someone,
- quickly explore responses while developing.

---

## Troubleshooting

### Problem: `python` not found

Solution: Install Python 3.11 or 3.12 from https://www.python.org/downloads/

### Problem: "scripts are disabled" when activating venv (PowerShell)

Solution: run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problem: dependency installation fails

Solution: upgrade pip:

```powershell
python -m pip install --upgrade pip
```

### Problem: `401 Unauthorized` from the provider API

Solution: verify that `EXCHANGERATE_API_KEY` is set correctly in your `.env` file.

---

## Additional references

- `app/settings.py` — settings loaded from `.env` and environment variables
- `DEPLOYMENT.md` — deployment + Postman guide
- `README.md` — project overview and API contract

---

## Providers

- `exchangerate_api` — real rates (requires an API key)
- `mock` — deterministic in-memory provider (no key required)

---

## Project structure

```text
Cur_ex_aiohttp_restful_api/
├── main.py                 # entry point
├── requirements.txt        # dependencies
├── .env                    # settings (created by you)
├── app/
│   ├── settings.py         # configuration
│   ├── app_factory.py      # app factory
│   ├── api/
│   ├── services/
│   │   └── exchange_service.py  # business logic
│   └── providers/
│       ├── exchangerate_api.py  # real provider
│       └── mock.py              # mock provider
└── tests/
```
