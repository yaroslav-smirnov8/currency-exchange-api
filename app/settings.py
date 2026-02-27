from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True, slots=True)
class Settings:
    provider_name: str
    exchangerate_api_key: str | None
    exchangerate_base_url: str
    http_timeout_seconds: float
    cors_enabled: bool
    cors_allowed_origins: list[str]

    @staticmethod
    def from_env() -> "Settings":
        env_path = Path(__file__).resolve().parents[1] / ".env"
        if env_path.exists():
            load_dotenv(env_path)

        provider_name = os.getenv("API_PROVIDER", "exchangerate_api").strip().lower()
        exchangerate_api_key = os.getenv("EXCHANGERATE_API_KEY") or os.getenv("API_KEY")
        exchangerate_base_url = os.getenv("EXCHANGERATE_BASE_URL", "https://v6.exchangerate-api.com/v6").rstrip("/")
        http_timeout_seconds = float(os.getenv("HTTP_TIMEOUT_SECONDS", "8.0"))

        cors_enabled = os.getenv("CORS_ENABLED", "true").strip().lower() in {"1", "true", "yes"}
        cors_allowed_origins_raw = os.getenv("CORS_ALLOWED_ORIGINS", "*").strip()
        cors_allowed_origins = [o.strip() for o in cors_allowed_origins_raw.split(",") if o.strip()]

        return Settings(
            provider_name=provider_name,
            exchangerate_api_key=exchangerate_api_key,
            exchangerate_base_url=exchangerate_base_url,
            http_timeout_seconds=http_timeout_seconds,
            cors_enabled=cors_enabled,
            cors_allowed_origins=cors_allowed_origins,
        )

