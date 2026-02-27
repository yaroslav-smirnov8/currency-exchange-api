from __future__ import annotations

from aiohttp import web

from app.errors import AppError, json_error_response
from app.settings import Settings


@web.middleware
async def error_middleware(request: web.Request, handler):
    try:
        return await handler(request)
    except AppError as exc:
        return json_error_response(exc)
    except web.HTTPException as exc:
        return web.json_response(
            {"error": {"code": "http_error", "message": exc.reason}},
            status=exc.status,
        )
    except Exception:
        return web.json_response(
            {"error": {"code": "internal_error", "message": "Unexpected server error."}},
            status=500,
        )


def cors_middleware(settings: Settings) -> web.middleware:
    allowed_origins = settings.cors_allowed_origins

    @web.middleware
    async def _middleware(request: web.Request, handler):
        if request.method == "OPTIONS":
            response = web.Response(status=204)
        else:
            response = await handler(request)

        origin = request.headers.get("Origin")
        if "*" in allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = "*"
        elif origin and origin in allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Vary"] = "Origin"

        response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        response.headers["Access-Control-Max-Age"] = "600"
        return response

    return _middleware

