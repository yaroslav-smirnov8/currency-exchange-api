from __future__ import annotations

from aiohttp import ClientSession, web

from app.api.middlewares import cors_middleware, error_middleware
from app.api.routes import register_routes
from app.providers.exchangerate_api import ExchangeRateApiProvider
from app.providers.mock import MockExchangeRateProvider
from app.services.exchange_service import ExchangeService
from app.settings import Settings


def create_app(settings: Settings | None = None) -> web.Application:
    resolved_settings: Settings = settings or Settings.from_env()

    middlewares = [error_middleware]
    if resolved_settings.cors_enabled:
        middlewares.append(cors_middleware(resolved_settings))

    app = web.Application(middlewares=middlewares)
    app["settings"] = resolved_settings

    async def _on_startup(app: web.Application) -> None:
        app["http_session"] = ClientSession()

        provider_name = resolved_settings.provider_name
        if provider_name == "mock":
            provider = MockExchangeRateProvider()
        elif provider_name == "exchangerate_api":
            provider = ExchangeRateApiProvider(
                http_session=app["http_session"],
                api_key=resolved_settings.exchangerate_api_key,
                base_url=resolved_settings.exchangerate_base_url,
                timeout_seconds=resolved_settings.http_timeout_seconds,
            )
        else:
            raise RuntimeError(f"Unknown provider: {provider_name}")

        app["exchange_service"] = ExchangeService(provider=provider, provider_name=provider_name)

    async def _on_cleanup(app: web.Application) -> None:
        session = app.get("http_session")
        if session is not None:
            await session.close()

    app.on_startup.append(_on_startup)
    app.on_cleanup.append(_on_cleanup)

    register_routes(app)
    return app
